import sys

# appending a path
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/')

# import urllib.request
# import urllib.parse
# import json
# #from diting.oia.graphs.pos_oia_graph import PosOIAGraph, ReCheckError, Stdandardizer
# from diting.oia.graphs.dependency_graph import DependencyGraph, UDGraphVisualizer
# from diting.oia.graphs.oia_graph import OIAGraph
#
# from data_processor.read_data import *
from UIDetector import  *
from PageDetector import *
from FeatureDetector import *
from Graph import *
from PIIDetector  import *

#first generate the graph using diting/diting/parser/sentence2multi/as_graph/client.py
def extractUIInfo(sent):
    UI_data = ui_detector(sent)
    return UI_data

def extractPageInfoBaseline(sent, doc_index):
    page_data = page_detector_baseline(sent, doc_index)
    return page_data

def extractPageInfo(sent, fileloc, sent_index_in_doc):
    page_data = process_parsed_description_for_page_wrapper(sent, fileloc, sent_index_in_doc)
    # page_data = page_detector(sent, doc_index)
    # print('Page Data', page_data)
    # print("-"*50)
    return page_data[0]

def extractFeatureInfo(sent, fileloc):
    # feature_data = feature_detector(sent)
    feature_data = process_parsed_description_for_feature_wrapper(sent, fileloc)
    return feature_data[0]

def extractFeatureUsingBaseline(sent, fileloc):

    feature_data = baseline_description_for_feature_wrapper(sent, fileloc)
    return feature_data[0]

def corelateExtractedInfoForSentence():
    infos = []
    return infos

def corelateExtractedInfoForDescription():
    infos = []
    return infos

def extractPII(sent):
    pii = pii_detector(sent)
    return pii


def collect_data():
    folder_loc = '/home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/ud/'
    loc = folder_loc + '*.json'

    data = []
    for file in glob.glob(loc):
        # print(file)
        objs = read_from_json(file)
        filename = file.split('/')[-1]
        filename = filename.split('.')[-2]

        txt_file = folder_loc + filename + '.txt'
        sent = read_from_txt(txt_file)

        # for obj in objs:
        objs[KEY_FILENAME] = filename
        objs[KEY_SENT] = sent
        data.append(objs)
        # print(objs)

        # break

    # print(data)

    return data

def create_graph_from_json(nodes_json, edges_json):

    node_dict ={}
    nodes = []
    edges = []
    for node in nodes_json:
        index = node[0]
        # ranges = node[1]
        type = node[2]
        nd = Node(index, type)
        nodes.append(nd)

    for edge in edges_json:
        elem = edge[0]
        src = elem[0]
        sink = elem[2]
        type = elem[1]

        edg = Edge(src, sink, type)
        edges.append(edg)

    graph = Graph()

    for edge in edges:
        graph.addEdge(edge.src, edge.sink)

# def run_rawdata():
#
#     data_list = collect_data()
#
#     result_data_list = []
#     for data in data_list:
#         sent = data[KEY_SENT].strip().lower()
#         UI_data = collectUIInfo(sent)
#         feature_data = extractFeatureInfo(sent)
#         page_data = extractPageInfo(sent)
#
#         data[KEY_PREDICTED_UI_ELEMENTS] = UI_data
#         data[KEY_PREDICTED_FEATURE] = feature_data
#         data[KEY_PREDICTED_PAGE] = page_data
#
#         result_data_list.append(data)
#
#
#     for data in result_data_list:
#         print(data)
#         print("*"*50)

def run_labeldata():
    data_list = get_label_data()
    print("Total Label Data: ", len(data_list))

    result_data_list = []

    match_ui = 0
    non_match_ui = 0
    non_match_ui_sentence = []

    match_current_page = 0
    non_match_current_page = 0
    non_match_current_page_sentence = []

    match_transition_page = 0
    non_match_transition_page = 0
    non_match_transition_page_sentence = []


    match_feature = 0
    non_match_feature = 0
    non_match_feature_sentences = []
    match_feature_sentences = []

    match_pii = 0
    non_match_pii = 0
    non_match_pii_sentences = []


    # ui_hot_encoder = {'TextView', 'EditText', 'Button', 'ImageButton', 'ToggleButton', 'RadioButton', 'RadioGroup',
    #             'CheckBox', 'AutoCompleteTextView', 'ProgressBar', 'Spinner', 'TimePicker', 'DatePicker',
    #             'SeekBar',
    #             'AlertDialog', 'Switch', 'switchbutton', 'RatingBar', 'Map', 'RadioButtonControl'}
    #
    # actual_ui_list = []
    # prediction_ui_list = []

    total_ui_elements = 0


    doc_feature = ''
    index = 0

    for tmp_data in data_list:
        data = tmp_data.copy()
        sentences = data[KEY_SENTENCES]
        doc_index = data[KEY_DOC_INDEX]
        filename = data[KEY_FILENAME]

        feature_predicted_dict = {} #track the predicted feature from each sentences, later consider the more frequent one
        tmp_sentences = []

        sent_index_in_doc = 1 #we want to start it from 1 to keep consistent with corref

        for elem in sentences:

            sent = elem[KEY_SENT].strip().lower()

            search_processed_file = 'oia_' + str(index) + '_' + filename


###############################processing UI information###################################
            # tp = 0
            # tn = 0
            # fp = 0
            # fn = 0
            #
            # ground_truth_ui_multi_class = {}
            # actual_multi_class = {}
            # prediction_multi_class = {}
            # uid = 0


            UI_data = extractUIInfo(sent)
            elem[KEY_PREDICTED_UI_ELEMENTS] = UI_data[KEY_PREDICTED_UI_ELEMENTS]
            ground_truth_ui = []
            for ui in elem[KEY_UI]:
                if len(ui[KEY_TYPE]) > 0:
                    ground_truth_ui.append(ui[KEY_TYPE])


            ground_truth_ui.sort()
            elem[KEY_PREDICTED_UI_ELEMENTS].sort()

            total_ui_elements += len(ground_truth_ui)

            flag = True
            for ui_real, ui_pred in zip(ground_truth_ui, elem[KEY_PREDICTED_UI_ELEMENTS]):
                if ui_pred.lower() != ui_real.lower():
                    flag = False
                    break


            if len(elem[KEY_PREDICTED_UI_ELEMENTS]) != len(ground_truth_ui) and len(ground_truth_ui)==0 and flag==True: #false positive
                flag = False

            if flag == True:
                match_ui += 1
                # tp+=len(elem[KEY_PREDICTED_UI_ELEMENTS])

            else:
                mispredict = {}
                mispredict['prediction'] = elem[KEY_PREDICTED_UI_ELEMENTS]
                mispredict['actual'] = ground_truth_ui
                mispredict['sent_index'] = elem[KEY_SENT_INDEX]

                non_match_ui += 1
                non_match_ui_sentence.append(mispredict)

################################################################################################
###############################processing PAGE information###################################

            if elem[KEY_PAGE][KEY_CURRENT] in  ['default']:
                elem[KEY_PAGE][KEY_CURRENT] = ''
            elem[KEY_PAGE][KEY_CURRENT] = elem[KEY_PAGE][KEY_CURRENT].lower()

            # ground_truth_current_page = elem[KEY_PAGE][KEY_CURRENT]
            # ground_truth_transition_page = elem[KEY_PAGE][KEY_TRANSITION]

            # page_data = extractPageInfoBaseline(sent, doc_index)
            page_data = extractPageInfo(sent, search_processed_file, sent_index_in_doc)
            # print(search_processed_file)

            # print('predicted page name:', page_data[KEY_PREDICTED_PAGE])


            elem[KEY_PREDICTED_PAGE] = {}
            elem[KEY_PREDICTED_PAGE][KEY_CURRENT] = page_data[KEY_PREDICTED_CURRENT_PAGE]
            elem[KEY_PREDICTED_PAGE][KEY_TRANSITION] = page_data[KEY_PREDICTED_TRANSITION_PAGE]


            page_prediction = {}
            page_prediction[KEY_SENT] = elem[KEY_SENT]
            page_prediction[KEY_PREDICTED_PAGE] = elem[KEY_PREDICTED_PAGE]
            page_prediction[KEY_CURRENT] = elem[KEY_PAGE]
            page_prediction[KEY_SENT_INDEX] = elem[KEY_SENT_INDEX]
            page_prediction[KEY_FILENAME] = elem[KEY_FILENAME]

            # data[KEY_PREDICTED_PAGE] = ''
            # if KEY_CURRENT in page_data:
            #     data[KEY_PREDICTED_PAGE] = page_data[KEY_CURRENT]

            if elem[KEY_PAGE][KEY_CURRENT] == elem[KEY_PREDICTED_PAGE][KEY_CURRENT] or len(elem[KEY_PAGE][KEY_CURRENT]) == len(elem[KEY_PREDICTED_PAGE][KEY_CURRENT]):
                match_current_page += 1
            else:
                non_match_current_page += 1
                non_match_current_page_sentence.append(page_prediction)


            if elem[KEY_PAGE][KEY_TRANSITION] == elem[KEY_PREDICTED_PAGE][KEY_TRANSITION] or len(elem[KEY_PAGE][KEY_TRANSITION]) == len(elem[KEY_PREDICTED_PAGE][KEY_TRANSITION]):
                match_transition_page += 1
            else:
                non_match_transition_page += 1
                non_match_transition_page_sentence.append(page_prediction)

            # elif len(elem[KEY_PAGE][KEY_CURRENT]) == len(elem[KEY_PREDICTED_PAGE][KEY_CURRENT])  len(elem[KEY_PAGE][KEY_TRANSITION]) and len(elem[KEY_PREDICTED_PAGE][KEY_TRANSITION]):
            #     match_page += 1
            # else:
            #     non_match_page += 1
            #     non_match_current_page_sentence.append(page_prediction)

################################################################################################
###############################processing PII information###################################
            pii_lst = extractPII(sent)
            elem[KEY_PREDICTED_PII] = pii_lst
            ground_truth_PII = []

            for pii_real in elem[KEY_PII].split(','):
                ground_truth_PII.append(pii_real.strip())

            # print(ground_truth_PII)
            # print(elem[KEY_PREDICTED_PII])

            ground_truth_PII.sort()
            elem[KEY_PREDICTED_PII].sort()



            flag = True
            for pii_real, pii_pred in zip(ground_truth_PII, elem[KEY_PREDICTED_PII]):
                if pii_real.lower() != pii_pred.lower():
                    flag = False
                    break

            if len(elem[KEY_PREDICTED_PII]) != len(ground_truth_PII) and len(
                    ground_truth_PII) == 0 and flag == True:  # false positive
                flag = False

            if flag == True:
                match_pii += 1
            else:
                mispredict = {}
                mispredict['prediction'] = elem[KEY_PREDICTED_PII]
                mispredict['actual'] = ground_truth_PII
                mispredict['sent_index'] = elem[KEY_SENT_INDEX]

                non_match_pii += 1
                non_match_pii_sentences.append(mispredict)



################################################################################################
###############################processing feature information###################################

            feature_data = extractFeatureInfo(sent, search_processed_file)
            # feature_data = extractFeatureUsingBaseline(sent, search_processed_file)


            if len(feature_data[KEY_PREDICTED_FEATURE]) > 0:
                # print('feature data', feature_data)
                # print('feature dict', feature_data[KEY_PREDICTED_FEATURE])
                if feature_data[KEY_PREDICTED_FEATURE] not in feature_predicted_dict:
                    feature_predicted_dict[feature_data[KEY_PREDICTED_FEATURE]] = 0
                feature_predicted_dict[feature_data[KEY_PREDICTED_FEATURE]] += 1
################################################################################################
            # data[KEY_SENT] = elem
            tmp_sentences.append(elem)
            index += 1
            sent_index_in_doc += 1

        data[KEY_SENT] = tmp_sentences
        result_data_list.append(data)


        sorted_list = sorted(feature_predicted_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse= True)

        data[KEY_PREDICTED_FEATURE] = ''
        if len(sorted_list) > 0:
            data[KEY_PREDICTED_FEATURE] = sorted_list[0][0]

        if data[KEY_FEAT] == data[KEY_PREDICTED_FEATURE]:
            match_feature += 1
            match_feature_sentences.append(data)
        else:
            non_match_feature += 1
            non_match_feature_sentences.append(data)



    print('UI')
    print('Total UI Elements:', total_ui_elements)
    print('Non Match ', non_match_ui)
    print('Match ', match_ui)
    print("*" * 50)

    print('Feature')
    print('Non Match ', non_match_feature)
    print('Match ', match_feature)
    print("*" * 50)


    print('page')
    print('Non Match Current', non_match_current_page)
    print('Match Current', match_current_page)

    print('Non Match Transition', non_match_transition_page)
    print('Match Transition', match_transition_page)

    print("*" * 50)


    print('pii')
    print('Non Match', non_match_pii)
    print('Match', match_pii)
    print("*"*50)



    write_to_json(non_match_ui_sentence, './prediction_output/ui_mismatch.json')
    write_to_json(non_match_current_page_sentence, './prediction_output/current_page_mismatch.json')
    write_to_json(non_match_transition_page_sentence, './prediction_output/transition_page_mismatch.json')

    write_to_json(non_match_feature_sentences, './prediction_output/feature_mismatch.json')
    write_to_json(match_feature_sentences, './prediction_output/feature_match.json')

    write_to_json(non_match_pii_sentences, './prediction_output/pii_detection.json')

    write_to_json(result_data_list, './prediction_output/information_extraction_results.json')


if __name__ == '__main__':
    run_labeldata()


