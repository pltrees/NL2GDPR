from helper.util import *
from helper.constant import *
import glob

def get_description_data():
    data = []
    for file in glob.glob("/home/faysal-gpu/code/intern/gdpr-code-generator/data/crowd_source_data/*.json"):
        print(file)
        objs = read_from_json(file)
        filename = file.split('/')[-1]
        filename = filename.split('.')[-2]

        for obj in objs:
            obj[KEY_FILENAME] = filename
        data += objs

    return data


def get_crowdsource_description_data(fileloc):
    data = []
    for file in glob.glob(fileloc):
        print(file)
        objs = read_from_json(file)
        filename = file.split('/')[-1]
        filename = filename.split('.')[-2]

        for obj in objs:
            obj[KEY_FILENAME] = filename
        data += objs

    return data


def get_purpose_data():
    fileloc = "/home/faysal-gpu/code/intern/gdpr-code-generator/data/purpose/generated_paraphrase.json"
    data = read_from_json(fileloc)
    return data


def get_template_purpose():
    fileloc = "/home/faysal-gpu/code/intern/gdpr-code-generator/data/purpose/template_purpose.json"
    data = read_from_json(fileloc)
    return data

def get_text_from_file(filename):
    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/purpose_ud/' + filename + '.txt'
    txt = read_from_txt(fileloc)
    return txt

def write_fluency_output(data):
    write_to_json(data, '/home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/fluency_tracker.json')

def write_purpose_with_readibility(data):
    write_to_json(data,
                  '/home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/readibility_tracker.json')


def write_generated_purposes(modified_list):
    # Serializing json
    json_object = json.dumps(modified_list, indent=4)
    # Writing to sample.json
    with open("/home/faysal-gpu/code/intern/gdpr-code-generator/data/purpose/generated_paraphrase.json", "w") as outfile:
        outfile.write(json_object)

def get_parsed_purpose_data():
    data = []
    for file in glob.glob("/home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/purpose_ud/*.json"):
        objs = read_from_json(file)
        filename = file.split('/')[-1]
        filename = filename.split('.')[-2]

        objs[KEY_FILENAME] = filename
        data += [objs]

    return data


def get_parsed_description_data():
    data = []
    for file in glob.glob("/home/faysal-gpu/code/intern/gdpr-code-generator/sota/oia_package/oia_package/desc_ud/*.json"):
        objs = read_from_json(file)
        filename = file.split('/')[-1]
        filename = filename.split('.')[-2]

        objs[KEY_FILENAME] = filename
        data += [objs]

    return data

def get_label_data():
    # fileloc = "/home/faysal-gpu/code/intern/gdpr-code-generator/data/data_for_labeling.json"
    fileloc = "/home/faysal-gpu/code/intern/gdpr-code-generator/data/data_for_labeling_crowd_source.json"
    datalist = read_from_json(fileloc)
    return datalist

def get_prediction_data_from_information_extractor():
    fileloc = "/home/faysal-gpu/code/intern/gdpr-code-generator/src/prediction_output/information_extraction_results.json"
    datalist = read_from_json(fileloc)
    return datalist


if __name__ == '__main__':
    get_description_data()