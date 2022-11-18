from helper.util import *
from data_processor.read_write_data import *

def check_data(data, lst):
    if len(data) > 0:
        tokens = data.split(".")
        if len(tokens) > 1:
            lst.append(data)
    return lst

def remove_quote(sent):
    sent = sent.replace("'","")
    sent = sent.replace('"', '')
    sent = sent.replace(",", "")
    return sent

def process_data(fileloc, version):

    csv_data = read_csv(fileloc)
    # print(csv_data[0])


    # v1
    # 12 = app description
    # 22 = app description
    # 30 = app description
    # 40 = app description
    # 50 = app description
    # 60 = app description
    # 70 = app description
    # 80 = app description
    # 90 = app description
    # 100 = app description

    lst = []

    if version == 1:
        for row in csv_data[5:]:
            lst = check_data(row[12], lst)
            lst = check_data(row[22], lst)
            lst = check_data(row[30], lst)
            lst = check_data(row[40], lst)
            lst = check_data(row[50], lst)
            lst = check_data(row[60], lst)
            lst = check_data(row[70], lst)
            lst = check_data(row[80], lst)
            lst = check_data(row[90], lst)
            lst = check_data(row[100], lst)
    # v2
    # 11 =  app description
    # 20 =  app description
    # 27 =  app description
    # 37 =  app description
    # 47 =  app description
    # 57 =  app description
    # 67 =  app description
    # 77 =  app description
    # 87 =  app description
    # 97 =  app description
    # 107 = app description
    # 117 = app description
    # 127 = app description

    if version == 2:
        for row in csv_data[5:]:
            lst = check_data(row[11], lst)
            lst = check_data(row[20], lst)
            lst = check_data(row[27], lst)
            lst = check_data(row[37], lst)
            lst = check_data(row[47], lst)
            lst = check_data(row[57], lst)
            lst = check_data(row[67], lst)
            lst = check_data(row[77], lst)
            lst = check_data(row[87], lst)
            lst = check_data(row[97], lst)
            lst = check_data(row[107], lst)
            lst = check_data(row[117], lst)
            lst = check_data(row[127], lst)

    write_to_json(lst, '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v2_16_jun_app_desc.json')

    print(len(lst))

    return lst

def create_data_for_labeling():
    datalist = get_crowdsource_description_data("/home/faysal-gpu/code/intern/gdpr-code-generator/data/crowd_source_data/part2/*.json")
    # sent_index = 0
    # doc_index = 0

    #for part 2
    sent_index = 300
    doc_index = 36

    modified_datalist = []

    for data in datalist:

        sentences = data[KEY_DESC].split(".")
        filename = data[KEY_FILENAME]

        lst = []
        for sent in sentences:
            if len(sent) < 1:
                continue

            sent_index += 1

            sent_dict = {}
            sent_dict[KEY_SENT] = sent
            sent_dict[KEY_SENT_INDEX] = sent_index
            sent_dict[KEY_UI] = [{
                KEY_TYPE: '',
                KEY_LABEL: ''
            }]
            sent_dict[KEY_PAGE] = {
                KEY_CURRENT: '',
                KEY_TRANSITION: '',
                KEY_LABEL: ''
            }
            sent_dict[KEY_PII] = ''
            sent_dict[KEY_FILENAME] = filename

            sent_dict[KEY_STORAGE] = ''
            sent_dict[KEY_PROCESS] = ''
            sent_dict[KEY_THIRD_PARTY_SHARE] = ''

            lst.append(sent_dict)

        data[KEY_SENTENCES] = lst
        data[KEY_DOC_INDEX] = doc_index
        doc_index += 1

        modified_datalist.append(data)

    # write_to_json(modified_datalist, '/home/faysal-gpu/code/intern/gdpr-code-generator/data/data_for_labeling.json')
    write_to_json(modified_datalist, '/home/faysal-gpu/code/intern/gdpr-code-generator/data/data_for_labeling_crowd_source_part_2.json')

def add_new_fields():

    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/data_for_labeling.json'
    datalist = read_from_json(fileloc)

    modified_datalist = []
    for data in datalist:

        sentences = data[KEY_SENTENCES]
        filename = data[KEY_FILENAME]

        lst = []
        for sent in sentences:

            if len(sent) < 1:
                continue

            sent_dict = sent
            sent_dict[KEY_STORAGE] = ''
            sent_dict[KEY_PROCESS] = ''
            sent_dict[KEY_THIRD_PARTY_SHARE] = ''

            lst.append(sent_dict)

        data[KEY_SENTENCES] = lst
        modified_datalist.append(data)

    write_to_json(modified_datalist, '/home/faysal-gpu/code/intern/gdpr-code-generator/data/data_for_labeling_modified.json')


if __name__ == '__main__':
    # fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v2_16_jun.csv'
    # version = 2
    # process_data(fileloc, version)
    create_data_for_labeling()
    # add_new_fields()