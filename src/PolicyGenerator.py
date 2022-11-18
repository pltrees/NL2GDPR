import sys

# appending a path
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/')
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/src/Paraphrase/paraphraser-master/paraphraser/')
from data_processor.read_write_data import *
from data_processor.constant import *
from inference import *
import nltk

from FluencyChecker import  *


def generate_paraphrases_from_templates():

    p = get_paraphraser()
    data_list = get_template_purpose()
    modified_list = []
    index = 0
    sent_index = 0
    for data in data_list:
        policies = data["policy"].split('.')
        lst = []
        for sent in policies:
            sent = sent.strip()
            if len(sent) < 1:
                continue
            tmp_dict = {}
            tmp_dict["sent_index"] = sent_index
            tmp_dict["original_sentence"] = sent
            sents = generate_paraphrase(sent, 0.80, 10, p)
            tmp_dict["generated_sentence"] = sents
            lst.append(tmp_dict)
            sent_index += 1
        data["generated_sentences"] = lst
        data["doc_index"] = index
        index += 1

        modified_list.append(data)

    write_generated_purposes(modified_list)

def is_original_file(filename):
    if '_original_' in filename:
        return True
    return False

def does_contain_PII(words):
    pii_list = get_PII()

    tokenizer = nltk.RegexpTokenizer(r"\w+") #remove all the punctuation
    words = tokenizer.tokenize(words)

    tokens = words.split()
    for token in tokens:
        if token in pii_list:
            return True
    return False

def process_parsed_purpose():
    data_list = get_parsed_purpose_data()

    modified_datalist = []
    original_node_dict = {}
    original_sent_dict = {}
    generated_node_dict = {}
    generated_sent_dict = {}
    fluency_tracker = []

    for data in data_list:
        filename = data[KEY_FILENAME]
        word_arr = {}
        graph = data["graph"]
        words = graph["words"]
        for word in words:
            word_arr[word[0]] = word[1]

        oia = graph["oia"]
        nodes = oia["nodes"]
        edges = oia["edges"]
        outgoing_edges_dict = {}
        incoming_edges_dict = {}

        for edge in edges:
            start_node = edge[0] #store the index of the node
            end_node = edge[2]
            label = edge[1]
            confidence = edge[3]

            if start_node not in outgoing_edges_dict:
                outgoing_edges_dict[start_node] = []
            outgoing_edges_dict[start_node].append(end_node)

            if end_node not in incoming_edges_dict:
                incoming_edges_dict[end_node] = []
            incoming_edges_dict[end_node].append(start_node)


        modified_nodes = []
        for node in nodes:
            node_id = node[0]
            node_count = len(node[1])
            words = ""

            type = node[2]
            words = words.lower().strip()
            words = words.replace('  ', ' ')

            for i in range(0, node_count):
                start_index = node[1][i][0]
                end_index = node[1][i][1]

                try:
                    start_index = int(start_index)
                except Exception as e:
                    # for appos
                    continue

                if start_index == end_index:
                    words = word_arr[start_index]
                else:
                    for index in range(start_index, end_index + 1):
                        words = words + '  '+ str(word_arr[index].strip())

                node_dict = {}
                node_dict['id'] = node_id
                node_dict['words'] = words
                node_dict['type'] = type
                node_dict['start_index'] = start_index
                node_dict['end_index'] = end_index

                modified_nodes.append(node_dict)

            words = words.lower().strip()
            words = words.replace('  ', ' ')
            words = words.replace("'", "")


            if type == 'noun':
                if is_original_file(filename):

                    words = words.replace('the ', '')
                    # words = words.replace('our ', '')
                    # words = words.replace('a ', '')
                    # words = words.replace('an ', '')
                    # words = words.replace('we ', '')

                    # we will only consider the representative nodes to be present in the generated nodes
                    if ((len(outgoing_edges_dict) + len(incoming_edges_dict) >= 2) or does_contain_PII(words)) \
                             and len(words.split(' ')) == 1:
                        # print("Representative Node")
                        if filename not in original_node_dict:
                            original_node_dict[filename] = []
                        original_node_dict[filename].append(words)

                else:
                    if filename not in generated_node_dict:
                        generated_node_dict[filename] = []
                    generated_node_dict[filename].append(words)



            # except Exception as e:
            #     print(e)
            #     continue
        data['modified_nodes'] = modified_nodes
        modified_datalist.append(data)



    # print(len(modified_datalist))

    is_consistent = False
    not_consistent_purposes = 0
    consistent_purpose = 0




    for f_orig, v_orig in original_node_dict.items():
        print("*" * 40)
        print(f_orig)
        tokens = f_orig.split('_')
        unique_name = '_'.join(tokens[2:-2])

        text_orig = get_text_from_file(f_orig)

        fluency_dict = {}
        # fluency_dict['original'] = text_orig
        fluency_dict['original'] = text_orig
        fluency_dict['filename'] = f_orig
        fluency_dict['scr'],_,_,_ = get_all_fluency_value(fluency_dict['original'])
        fluency_tracker.append(fluency_dict)

        lst = []

        if len(v_orig) == 0:
            for f_gen, v_gen in generated_node_dict.items():
                if unique_name in f_gen:
                    fluency_dict = {}
                    fluency_dict['generated'] = get_text_from_file(f_gen)
                    fluency_dict['original'] = text_orig
                    fluency_dict['filename'] = f_gen
                    fluency_dict['scr'], dcr, gf, fre = get_all_fluency_value(fluency_dict['generated'])

                    result_dict = check(dcr, gf, fre, {})
                    fluency_dict['is_added'] = result_dict['is_selected']
                    # fluency_dict.update(check(dcr, gf, fre, {}))
                    fluency_tracker.append(fluency_dict)

                    lst.append(f_gen)

        for f_gen, v_gen in generated_node_dict.items():
            if unique_name in f_gen:

                for wrd_o in v_orig:
                    is_consistent = 0
                    for wrd_g in v_gen:
                        if wrd_o in wrd_g:
                            is_consistent += 1
                    # if is_consistent == False:
                    #     break
                if is_consistent >= len(v_orig)-1:

                    fluency_dict = {}
                    fluency_dict['generated'] = get_text_from_file(f_gen)
                    fluency_dict['original'] = text_orig
                    fluency_dict['filename'] = f_gen
                    fluency_dict['scr'], dcr, gf, fre = get_all_fluency_value(fluency_dict['generated'])

                    result_dict = check(dcr, gf, fre, {})
                    fluency_dict['is_added'] = result_dict['is_selected']
                    # fluency_dict.update(check(dcr, gf, fre, {}))
                    fluency_tracker.append(fluency_dict)

                    lst.append(f_gen)

                    consistent_purpose += 1

                else:

                    # print("-"*50)
                    # print('original', v_orig)
                    # print('generated', v_gen)
                    # print("-" * 50)

                    not_consistent_purposes += 1



        # print(lst)

    print("Total Not consistent = ", not_consistent_purposes)
    print("Total Added=", consistent_purpose)
    write_fluency_output(fluency_tracker)


    return modified_datalist



if __name__ == '__main__':
    # i selected this environment -- py36-2
    # generate_paraphrases_from_templates()
    process_parsed_purpose()