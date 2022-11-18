from data_processor.preprocess import *
import os

def format_slot_intent_data(item, fileloc):

    elements = ['TextView', 'EditText', 'Button', 'ImageButton', 'ToggleButton', 'RadioButton', 'RadioGroup', 'CheckBox', 'AutoCompleteTextView', 'ProgressBar', 'Spinner', 'TimePicker', 'DatePicker', 'SeekBar', 'AlertDialog', 'Switch', 'RatingBar']
    features = ['login', 'logout', 'register', 'forget password', 'status', 'share', 'profile', 'third-party', 'advertisement', 'connections', 'newsfeed', 'analytics']
    # events = ['press', 'long pressed']
    # Data = [username, firstname, lastname, name, email, mail, address, country, state, zipcode, city, county, age,
    #        location, birthdate, ipaddress]

    tokens = item.split(" ")
    for token in tokens:
        if len(token) > 0:
            end_tag = ' O\n'
            for elem in elements:
                if elem.lower() in token.lower() :
                    end_tag = ' B-ui\n'
            for feature in features:
                if feature.lower() in token.lower():
                    end_tag = ' B-feature\n'

            token = token + end_tag
            write_to_txt(token, fileloc, 'a')

    write_to_txt('\n', fileloc, 'a')

def delete_previously_generated_file(fileloc):
    os.remove(fileloc)

if __name__ == '__main__':
    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v1_16_jun.csv'
    version = 1
    lst1 = process_data(fileloc, version)

    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v2_16_jun.csv'
    version = 2
    lst2 = process_data(fileloc, version)

    train_ratio = .4
    dev_ratio = .3
    test_ratio = .3

    total_data = lst1 + lst2
    total_len = len(total_data)
    train_size = train_ratio * total_len
    test_size =  test_ratio * total_len
    dev_size =  total_len * dev_ratio


    train_text_file= '/home/faysal-gpu/code/intern/gdpr-code-generator/data/train.txt'
    test_text_file = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/test.txt'
    dev_text_file = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/dev.txt'

    delete_previously_generated_file(train_text_file)
    delete_previously_generated_file(test_text_file)
    delete_previously_generated_file(dev_text_file)


    count = 0
    for item in total_data:
        if train_size > 0 :
            format_slot_intent_data(item, train_text_file)
            train_size -= 1
        elif test_size > 0:
            format_slot_intent_data(item, test_text_file)
            test_size -= 1
        elif dev_size > 0:
            format_slot_intent_data(item, dev_text_file)
            dev_size -= 1
        count += 1
