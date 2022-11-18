import sys

# appending a path
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/')
from data_processor.read_write_data import *


def run():
    data_list = get_label_data()

    for data in data_list:
        desc = (data['desc'])
        doc_index = data['doc_index']
        filename = data['filename']

        write_to_txt(desc, '/home/faysal-gpu/code/intern/gdpr-code-generator/sota/coref_tool/conll-2012/data/initial_data/'+ str(doc_index) +'__' + filename + '.txt', 'w')


if __name__ == '__main__':
    run()
