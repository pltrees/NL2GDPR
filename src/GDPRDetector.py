from data_processor.preprocess import *
from PIIDetector import *

def process_individual_description(data, input_feature):
    filename = data[KEY_FILENAME]
    word_arr = {}
    graph = data["graph"]
    words = graph["words"]
    for word in words:
        word_arr[word[0]] = word[1]

    oia = graph["oia"]
    edges = oia["edges"]
    nodes = oia["nodes"]
    lst_events = []
    lst_pii = []

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
            # print('Event Words: ', words)
            lst_events += gdpr_detector(words, input_feature)

        if type == 'noun':
            if 'page' not in words:
                # print('words:', words)
                piis = pii_detector(words)
                # print("PII", piis)
                lst_pii += piis


    #should we use corref tool to detect the relation with the event and noun?

    node_dict = {}
    node_dict[KEY_FILENAME] = filename
    node_dict[KEY_STORAGE] = ""
    node_dict[KEY_PROCESS] = ""
    node_dict[KEY_THIRD_PARTY_SHARE]= ""

    if len(lst_pii) > 0:
        for opr in lst_events:
            print(opr, '->', lst_pii)
            node_dict[opr] = lst_pii
    return node_dict




def process_parsed_description_for_gdpr_wrapper(sent, input_feature, fileloc):
    data_list = get_parsed_description_data()

    modified_nodes = []

    for data in data_list:
        if data[KEY_FILENAME] == fileloc:
            node_dict = process_individual_description(data, input_feature)
            modified_nodes.append(node_dict)

    return modified_nodes[0]


# def baseline_description_for_feature_wrapper(sent, fileloc):
#
#     features = feature_detector(sent)
#
#     node_dict = {}
#     node_dict[KEY_FILENAME] = fileloc
#
#     node_dict[KEY_PREDICTED_FEATURE] = []
#     if len(features) > 0:
#         node_dict[KEY_PREDICTED_FEATURE] = features[0]
#     return [node_dict]



def gdpr_detector(sent, input_feature):

    if len(sent) < 1:
        return []


    events = {
        'storage': ['Store', 'Save', 'Upload', 'Register', 'Create', 'Record'],
        'process' : ['Show', 'View', 'Display', 'Exhibit'],
        'thirdpartysharing': ['Share', 'Send'],
    }

    features = {
        'storage': ['registration', 'user profile', 'status updates', 'water recorder','food recorder', 'summary of the day', 'comments', 'address book', 'change password', 'user status', 'blog writing', 'add new friends', 'notes'],
        'process': ['news feed', 'summary of the day', 'comments', 'address book', 'login', 'people nearby', 'chat with friends', 'user friends list', 'search for people nearby', 'app purchase', 'share', 'review'],
        'thirdpartysharing': ['third-party integrations', 'app purchase', 'share', 'advertisement']
    }


    feature_list = []
    operations = []

    for key, values in features.items():
        for val in values:
            val = val.lower()
            if val == input_feature.lower():
                feature_list.append(remove_quote(key))
                operations.append(key)

    final_pred = []

    tokens = sent.split(' ')
    for token in tokens:
        token = token.lower()
        token = remove_quote(token)

        for opr in operations:
            for event in events[opr]:
                if token == event.lower():
                    final_pred.append(opr)

    # print("final Predicton", final_pred)
    return final_pred



if __name__ == '__main__':
    # str = "In 'registration' page, the user only needs to input their email address in 'edittext' and hit the 'sign up' button"
    # str = "When user enter the 'registration' page, the app should show a group of TextView and EditText pairs: <'User Name',"
    # # str = " Then they will be sent to a page that reminds them to hit the activation link from their email boxes"
    # # str = " After the activation link is hit, the users will be automatically sent to the main page"
    #
    # lst = feature_detector(str)
    # print(lst)

    # lst = process_parsed_description_for_feature()
    # write_to_json(lst, '/home/faysal-gpu/code/intern/gdpr-code-generator/src/feature_output/feature.json')

    # print("finished", "*"*100)
    # lst = process_parsed_description_for_feature_wrapper('', 'oia_73_3_create_new_post')
    # print(lst)

    lst = gdpr_detector("Click the button of  'continue', the system will send the user's 'email' and 'password' to the server and jump to the 'registration complete' page", "registration")
    # print(lst)
