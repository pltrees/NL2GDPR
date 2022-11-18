from data_processor.preprocess import *


# process coref output to remove irrelevant information
def process_coref_output():
    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/output/coref.json'
    datalist= read_from_json(fileloc)

    # print("Doc Token", modified_word, filename, idx_sent, original_word)

    modified_data_list = []
    for data in datalist:
        data[KEY_MODIFIED_PAGE_COREF_INFO] = ''

        page_name = ''
        for sent in data[KEY_MENTION_STR]:

            tokens = sent.split("'")
            if len(tokens) == 3:
                if 'page' in tokens[2] and 'button' not in tokens[2]:
                    page_name = tokens[1].lower().strip()
                    data[KEY_MODIFIED_PAGE_COREF_INFO] = page_name
                    break


        #     # handle nouns where more than one word present
        #     sent = sent.replace("'", "  '  ") #need to incorporate this due to the error in corref processing
        #
        #     tokens = sent.split(" ")
        #     page_name = ''
        #     stack_enable = False
        #     concrete_page_name_found = False
        #
        #
        #     if len(tokens) > 2:
        #         for token in tokens:
        #             token = token.strip()
        #
        #             if stack_enable == True:
        #                 page_name += token + ' '
        #
        #             if "'" in token:
        #                 if stack_enable:
        #                     concrete_page_name_found = True
        #                     break
        #                 stack_enable = not stack_enable
        #
        #
        # if concrete_page_name_found == True:
        #     page_name = page_name.replace("'","")
        #     page_name = page_name.lower().strip()
        #     data[KEY_MODIFIED_COREF_INFO] = page_name

        tmp = data.copy()
        modified_data_list.append(tmp)



        # doc_index = data[KEY_DOC_INDEX] # "doc_index": "2__5_registration.txt",
        # doc_token = doc_index.split('__') [1]
        # doc_token = doc_token.split('.')[0]
        #
        #
        #
        # data[KEY_MODIFIED_COREF_INFO] = ''
        #
        #
        # if filename == doc_token and idx_sent in data[KEY_MENTION_SENTENCES]:
        #     header = data[KEY_MENTION_STR][0].lower().strip()
        #     if header == original_word:
        #         data[KEY_MODIFIED_COREF_INFO] = modified_word
        #         print("Modified Coref", modified_word)



    output_fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/output/output_coref.json'
    write_to_json(modified_data_list, output_fileloc)

def find_in_coref(extracted_coref_info, idx_sent, filename):

    for data in extracted_coref_info:

        doc_index = data[KEY_DOC_INDEX] # "doc_index": "2__5_registration.txt",
        doc_token = doc_index.split('__') [1]
        doc_token = doc_token.split('.')[0]

        # print('doctoken', doc_token)
        # print(filename)

        for idx in data[KEY_MENTION_SENTENCES]:
            if doc_token in filename:
                # print('idx', idx, 'idx sent', idx_sent)
                if int(idx) == int(idx_sent):

                    extracted_name = data[KEY_MODIFIED_PAGE_COREF_INFO]
                    if len(extracted_name) > 0:
                        return extracted_name

        # print("*"*50)

    return None



def process_individual_description(data, extracted_coref_info, sent_index_in_doc):
    # print('data', data)
    filename = data[KEY_FILENAME]
    word_arr = {}
    graph = data["graph"]
    words = graph["words"]
    for word in words:
        word_arr[word[0]] = word[1]

    oia = graph["oia"]
    edges = oia["edges"]
    nodes = oia["nodes"]
    lst = []

    sent_index = filename.split('_')[1]

    transition_detected = False

    for node in nodes:
        node_id = node[0]
        node_count = len(node[1])
        words = ""
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
                for index in range(start_index, end_index+1):
                    words = words + '  ' + str(word_arr[index].strip())
        type = node[2]

        words = words.lower().strip()
        words = words.replace('  ', ' ')

        if type == 'event':
            transition_keywords = ['jump', 'return', 'take', 'go', 'transition', 'trigger']
            for tk in transition_keywords:
                if tk in words:
                    transition_detected = True

        if type == 'noun':
            if 'page' in words:
                # print('Printing the words:', words)
                page_name = ''
                info = find_in_coref(extracted_coref_info, sent_index_in_doc, filename)
                if info:
                    page_name = info
                else:
                    # print("Pagename", page_name)

                    # tokens = words.split("'")
                    # if len(tokens) > 2:
                    #     if 'page' in tokens[2] and 'button' not in tokens[2]:
                    #         page_name = tokens[1].lower().strip()
                    #         # page_name = page_name

                    # #handle nouns where more than one word present
                    tokens = words.split(' ')
                    stack_enable = False

                    if len(tokens) > 2:
                        for token in tokens:
                            token = token.strip()

                            if stack_enable == True:
                                page_name += token + ' '

                            if "'" in token:
                                stack_enable = not stack_enable

                    else:
                        page_name = words.replace(' page', '')
                        page_name = page_name.replace('the ', '')
                        page_name = page_name.replace('a ', '')
                        page_name = page_name.strip()

                if page_name in ['the', 'any']:
                    page_name = ''

                page_name = page_name.replace('the ', '')
                page_name = page_name.replace('a ', '')
                page_name = page_name.replace("'", "")
                page_name = page_name.strip()
                if len(page_name)>0:
                    lst.append(page_name)

                    # print('Extracted Page Name:', page_name)



    #need to detect whether it is transition or current page

    node_dict = {}
    node_dict[KEY_FILENAME] = filename
    node_dict[KEY_PREDICTED_CURRENT_PAGE] = ''
    node_dict[KEY_PREDICTED_TRANSITION_PAGE] = ''

    if len(lst) == 2 and transition_detected == True:
        node_dict[KEY_PREDICTED_CURRENT_PAGE] = lst[0]
        node_dict[KEY_PREDICTED_TRANSITION_PAGE] = lst[1]

    elif transition_detected == True and len(lst) > 2:
        node_dict[KEY_PREDICTED_CURRENT_PAGE] = lst[0]
        page_list = ', '.join(lst[1:])
        node_dict[KEY_PREDICTED_TRANSITION_PAGE] = page_list

    elif transition_detected == True:
        if len(lst) > 0:
            node_dict[KEY_PREDICTED_TRANSITION_PAGE] = lst[0]
    else:
        if len(lst) > 0:
            node_dict[KEY_PREDICTED_CURRENT_PAGE] = lst[0]

    # print('returned node_dict value:', node_dict)
    # print('*' * 50)

    return node_dict

def get_pageinfo_using_coref(doc_index, page_title):
    data_list = read_from_json('/home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/output/coref.json')

    for data in data_list:
        if data['doc_index'] == str(doc_index) + ".txt":
            for mention_str in data['mention_strs']:
                if mention_str == page_title:
                    coref_page_info = page_detector_baseline(data['mention_strs'][0])
                    return coref_page_info


def process_parsed_description_for_page_wrapper(sent, fileloc, sent_index_in_doc):
    data_list = get_parsed_description_data()
    modified_nodes = []

    process_coref_output()
    extracted_coref_info = read_from_json('/home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/output/output_coref.json')

    for data in data_list:
        if data[KEY_FILENAME] == fileloc:
            # print(fileloc)
            node_dict = process_individual_description(data, extracted_coref_info, sent_index_in_doc)
            modified_nodes.append(node_dict)
            break

    return modified_nodes


def page_detector(sent, doc_index=-1):

    return

def page_detector_baseline(sent, doc_index=-1):

    tokens = sent.split()
    # print(tokens)

    stack = []
    stack_enable = False

    pages = []


    # for token in tokens:
    for iter in range(len(tokens)):

        token = tokens[iter]
        token = token.strip()

        if token == "'":
            if stack_enable:
                stack = []
            stack_enable = not stack_enable


        if stack_enable:
            stack.append(token)

        if token == 'page' or token == 'page,':
            page_dict = {}
            if len(stack) > 0:
                page_dict[KEY_CURRENT] = remove_quote(stack.join(' '))
            elif iter > 0 and doc_index != -1:
                #extract using coref
                page_dict[KEY_CURRENT] =  get_pageinfo_using_coref(doc_index, tokens[iter-1])
                # page_dict[KEY_CURRENT] =  remove_quote(tokens[iter-1])

            pages.append(page_dict)

    return  pages



if __name__ == '__main__':
    str1 = "In 'registration' page, the user only needs to input their email address in 'edittext' and hit the 'sign up' button"
    # str1 = " Then they will be sent to a page that reminds them to hit the activation link from their email boxes"
    # str1 = " After the activation link is hit, the users will be automatically sent to the main page"

    lst = page_detector_baseline(str1)
    print(lst)


