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
from GDPRDetector import *



def run_labeldata():
    data_list = get_prediction_data_from_information_extractor()
    print("Total Label Data: ", len(data_list))

    result_data_list = []


    doc_feature = ''
    index = 0

    match_storage = 0
    non_match_storage = 0

    tp_storage = 0
    tn_storage = 0
    fp_storage = 0
    fn_storage = 0

    mismatch_storage_sentences = []

    match_process = 0
    non_match_process = 0

    tp_process = 0
    tn_process = 0
    fp_process = 0
    fn_process = 0

    mismatch_process_sentences = []

    match_share = 0
    non_match_share = 0

    tp_share = 0
    tn_share = 0
    fp_share = 0
    fn_share = 0

    mismatch_share_sentences = []

    for tmp_data in data_list:
        data = tmp_data.copy()
        sentences = data[KEY_SENTENCES]
        doc_index = data[KEY_DOC_INDEX]
        filename = data[KEY_FILENAME]

        tmp_sentences = []

        input_feature = data[KEY_PREDICTED_FEATURE]

        input_feature = data[KEY_FEAT]

        pred_gdpr = {}

        for elem in sentences:

            sent = elem[KEY_SENT].strip().lower()
            search_processed_file = 'oia_' + str(index) + '_' + filename
            output = process_parsed_description_for_gdpr_wrapper(sent, input_feature, search_processed_file)

            # print('Output from GDPR Policy Finder: ', output)

            pred_gdpr = {}
            pred_gdpr[KEY_DOC_INDEX] = doc_index
            pred_gdpr[KEY_SENT] = sent
            pred_gdpr[KEY_FILENAME] = filename
            pred_gdpr[KEY_STORAGE] = elem[KEY_STORAGE]
            pred_gdpr[KEY_PROCESS] = elem[KEY_PROCESS]
            pred_gdpr[KEY_THIRD_PARTY_SHARE] = elem[KEY_THIRD_PARTY_SHARE]

            pred_gdpr[KEY_PII] = elem[KEY_PII]
            pred_gdpr[KEY_PREDICTED_FEATURE] = data[KEY_PREDICTED_FEATURE]
            pred_gdpr[KEY_FEAT] =  data[KEY_FEAT]


            pred_gdpr[KEY_PRED_STORAGE] = output[KEY_STORAGE]
            pred_gdpr[KEY_PRED_PROCESS] = output[KEY_PROCESS]
            pred_gdpr[KEY_PRED_THIRD_PARTY_SHARE] = output[KEY_THIRD_PARTY_SHARE]

            if pred_gdpr[KEY_STORAGE] == pred_gdpr[KEY_PRED_STORAGE]:
                match_storage += 1
                if len(pred_gdpr[KEY_PII]) > 0:
                    tp_storage += 1
                else:
                    tn_storage += 1
            else:
                non_match_storage += 1
                mismatch_storage_sentences.append(pred_gdpr)

                if len(pred_gdpr[KEY_PII]) > 0:
                    fp_storage += 1
                else:
                    fn_storage += 1


            if pred_gdpr[KEY_PROCESS] == pred_gdpr[KEY_PRED_PROCESS]:
                match_process += 1
                if len(pred_gdpr[KEY_PII]) > 0:
                    tp_process += 1
                else:
                    tn_process += 1
            else:
                non_match_process += 1
                mismatch_process_sentences.append(pred_gdpr)

                if len(pred_gdpr[KEY_PII]) > 0:
                    fp_process += 1
                else:
                    fn_process += 1


            if pred_gdpr[KEY_THIRD_PARTY_SHARE] == pred_gdpr[KEY_PRED_THIRD_PARTY_SHARE]:
                match_share += 1

                if len(pred_gdpr[KEY_PII]) > 0:
                    tp_share += 1
                else:
                    tn_share += 1
            else:
                non_match_share += 1
                mismatch_share_sentences.append(pred_gdpr)

                if len(pred_gdpr[KEY_PII]) > 0:
                    fp_share += 1
                else:
                    fn_share += 1



################################################################################################
            tmp_sentences.append(elem)
            index += 1

        # data[KEY_SENT] = tmp_sentences
        result_data_list.append(data)




    write_to_json(result_data_list, './prediction_output/gdpr_policy_finder_results.json')

    write_to_json(mismatch_storage_sentences, './prediction_output/mismatch_storage.json')
    write_to_json(mismatch_process_sentences, './prediction_output/mismatch_process.json')
    write_to_json(mismatch_share_sentences, './prediction_output/mismatch_share.json')


    print('Storage')
    print('Non Match', non_match_storage)
    print('Match', match_storage)


    print('TP_STORAGE', tp_storage)
    print('TN_STORAGE', tn_storage)
    print('FP_STORAGE', fp_storage)
    print('FN_STORAGE', fn_storage)

    calculate_doc_performance(mismatch_storage_sentences, "storage doc")
    print("*" * 50)


    print('Process')
    print('Non Match', non_match_process)
    print('Match', match_process)


    print('TP_PROCESS', tp_process)
    print('TN_PROCESS', tn_process)
    print('FP_PROCESS', fp_process)
    print('FN_PROCESS', fn_process)
    calculate_doc_performance(mismatch_process_sentences, "process doc")
    print("*"*50)

    print('Share')
    print('Non Match', non_match_share)
    print('Match', match_share)


    print('TP_SHARE', tp_share)
    print('TN_SHARE', tn_share)
    print('FP_SHARE', fp_share)
    print('FN_SHARE', fn_share)
    calculate_doc_performance(mismatch_share_sentences, "share doc")
    print("*"*50)


def calculate_doc_performance(lst, tag):

    doc ={}
    for data in lst:
        doc_index = data[KEY_DOC_INDEX]
        doc[doc_index] = 0

    print(tag, len(doc))

if __name__ == '__main__':
    run_labeldata()


