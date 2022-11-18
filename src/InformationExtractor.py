import sys

# appending a path
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/')
from data_processor.read_write_data import *


def process_parsed_description():
    data_list = get_parsed_description_data()

    modified_datalist = []

    for data in data_list:
        # print(data)
        filename = data[KEY_FILENAME]
        word_arr = {}
        graph = data["graph"]
        words = graph["words"]
        for word in words:
            word_arr[word[0]] = word[1]
        print(word_arr)
        oia = graph["oia"]
        nodes = oia["nodes"]

        modified_nodes = []
        for node in nodes:
            print(filename)
            node_id = node[0]
            try:
                start_index = node[1][0][0]
                end_index = node[1][0][1]
                words = ""
                if start_index == end_index:
                    words = word_arr[start_index]
                else:
                    for index in range(start_index, end_index):
                        words = words + '  ' + str(word_arr[index])
                        print(start_index)
                        print(end_index)
                        print(index)
                        print(word_arr)
                        print(words)
                type = node[2]

            except Exception as e:
                continue

            node_dict = {}
            node_dict['id'] = node_id
            node_dict ['words'] = words
            node_dict['type'] = type
            node_dict['start_index' ] =start_index
            node_dict['end_index'] = end_index

            modified_nodes.append(node_dict)

        edges = oia["edges"]
        data['modified_nodes' ] =modified_nodes
        modified_datalist.append(data)

    print(len(modified_datalist))
    return modified_datalist


if __name__ == '__main__':
    process_parsed_description()