from data_processor.preprocess import *

def process_individual_description(data):
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
                # start_index = node[1][1][0]
                # end_index = node[1][1][1]

            # print(filename)
            # print(node_id)
            # print("Start Index", start_index)
            # print("End Index", end_index)
            # print("Node Count", node_count)
            # print("*"*50)

            if start_index == end_index:
                words = word_arr[start_index]
            else:
                for index in range(start_index, end_index):
                    words = words + '  ' + str(word_arr[index].strip())
            type = node[2]

        words = words.lower().strip()
        words = words.replace('  ', ' ')
        if type == 'noun':
            # print('Words: ', words)
            lst += feature_detector(words)

    # print(filename)
    # print(lst)
    # print(data)
    # print("*" * 50)
    # find the occurence of the features in case of more than one feature
    ftr_dict = {}
    for ftr in lst:
        if ftr not in ftr_dict:
            ftr_dict[ftr] = 0
        ftr_dict[ftr] += 1

    sorted_list = sorted(ftr_dict.items(), key=lambda kv: (kv[0], kv[1]))

    node_dict = {}
    node_dict[KEY_FILENAME] = filename

    node_dict[KEY_PREDICTED_FEATURE] = []
    if len(sorted_list) > 0:
        node_dict[KEY_PREDICTED_FEATURE] = sorted_list[0][0]
    return node_dict


def match_parsed_description_with_given_sent(sent):
    data_list = get_parsed_description_data()
    for data in data_list:
        sent = sent.lower()
        sent = sent.strip()




def process_parsed_description_for_feature_wrapper(sent, fileloc):
    data_list = get_parsed_description_data()

    modified_nodes = []

    for data in data_list:
        if data[KEY_FILENAME] == fileloc:
            node_dict = process_individual_description(data)
            modified_nodes.append(node_dict)

    return modified_nodes


def baseline_description_for_feature_wrapper(sent, fileloc):

    features = feature_detector(sent)

    node_dict = {}
    node_dict[KEY_FILENAME] = fileloc

    node_dict[KEY_PREDICTED_FEATURE] = []
    if len(features) > 0:
        node_dict[KEY_PREDICTED_FEATURE] = features[0]
    return [node_dict]





def process_parsed_description_for_feature():
    data_list = get_parsed_description_data()

    modified_nodes = []

    for data in data_list:
        node_dict = process_individual_description(data)
        modified_nodes.append(node_dict)

    return modified_nodes


def feature_detector(sent):

    if len(sent) < 1:
        return []

    features = ['registration', 'user profile', 'status updates', 'news feed', 'water recorder','food recorder', 'summary of the day', 'healthy recipes', 'comments',
'address book', 'login', 'change password', 'people nearby', 'say hi', 'newsfeed', 'logout', 'forget password', 'third-party integrations', 'notifications',
'chat with friends', 'emoticon input', 'user status', 'user friends list', 'blog writing', 'product scan',
'clock setting', 'news recommendation', 'search for people nearby', 'add new friends', 'process request of creating friendship', 'app purchase', 'Third-Party Data Sharing',
                'share', 'review', 'notes']

    features = {
        'registration': ['registration', 'sign up'],
        'user profile' : ['user profile'],
        'status updates': ['status updates'],
        'news feed': ['news feed'],
        'home feed': ['home feed'],
        'water recorder': ['water recorder'],
        'food recorder': ['food recorder'],
        'summary of the day': ['summary of the day'],
        'healthy recipes': ['healthy recipes'],
        'comments': ['comments'],
        'address book': ['address book'],
        'login' : ['login'],
        'change password' : ['change password', 'forgot password'],
        'people nearby' : ['people nearby'],
        'say hi' : ['say hi'],
        # 'logout' : ['logout'],
        # 'forget password',
        'third-party integrations' : ['third-party integrations', 'third-party', 'Third-Party Data Sharing'],
        # 'notifications' : ['notifications'],
        'chat with friends' : ['chat with friends',  'user friends list', 'process request of creating friendship'] ,
        'add new friends' : ['add new friends'],
        'emoticon input' : ['emoticon input'],
        'user status' : ['user status'],
        'blog writing' : ['blog writing'],
        'product scan' : ['product scan'],
        'clock setting' : ['clock setting', 'clock'],
        'news recommendation' : ['news recommendation'],
        'search for people nearby' : ['search for people nearby', 'people nearby'],
        'app purchase' : ['app purchase'],
        'share' : ['share'],
        'review' : ['review'],
        'notes' : ['note'],
        'create new post' : ['create new post', 'new post', 'write post', 'create a new post', 'posting']
    }

    # data = {}
    # # data[KEY_SENT] = sent
    # data[KEY_PREDICTED_FEATURE] = []

    feature_list = []

    for key, values in features.items():
        for val in values:
            val = val.lower()
            if val in sent.lower():
                feature_list.append(remove_quote(key))

                # return feature_list


    return feature_list



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

    print("finished", "*"*100)
    lst = process_parsed_description_for_feature_wrapper('', 'oia_73_3_create_new_post')
    print(lst)

