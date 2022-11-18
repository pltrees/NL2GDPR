from data_processor.preprocess import *
from nltk.stem.lancaster import LancasterStemmer

def detect(desc):
    lst = []
    sentences = desc.split('.')
    for iter in range(len(sentences)):
        sent = sentences[iter]
        sent = sent.strip()
        elem  = ui_detector(sent)
        lst.append(elem)
    return  lst

def ui_detector(sent):
    '''if we explore with OIA then it will help us to avoid event. For example, registration process wont be detected as noun. so it will help us to avoid FP'''
    '''
       UI Elements: [TextView, EditText, Button, ImageButton, ToggleButton, RadioButton, RadioGroup, CheckBox, AutoCompleteTextView, ProgressBar, Spinner, TimePicker, DatePicker, SeekBar, AlertDialog, Switch, RatingBar]
   **To learn more about UI elements, visit here: data-flair.training/blogs/android-ui-controls/.
   Events: [press, long pressed]
   **To learn more about events, visit here: developer.android.com/guide/topics/ui/ui-events.
   Resource: [image, text, video]
   Data: [username, firstname, lastname, name, email, mail, address, country, state, zipcode, city, county, age, location, birthdate, ipaddress]
       '''

    elements = ['TextView', 'EditText', 'Button', 'ImageButton', 'ToggleButton', 'RadioButton', 'RadioGroup',
                'CheckBox', 'AutoCompleteTextView', 'ProgressBar', 'Spinner', 'TimePicker', 'DatePicker', 'SeekBar',
                'AlertDialog', 'Switch', 'switchbutton', 'RatingBar', 'Map', 'RadioButtonControl']

    ui_elements = []
    # for token in tokens:
    # for iter in range(len(tokens)):
        # token = tokens[iter]

    st = LancasterStemmer()

    data = {}
    # data[KEY_SENT] = sent
    data[KEY_PREDICTED_UI_ELEMENTS] = []

    # data[TAG_PAGE_NAME] = ""

    # if 'page' in token and iter > 0:
    #     data[TAG_PAGE_NAME] = tokens[iter - 1]


    tokens = sent.split(' ')

    for sent in tokens:
        sent = sent.lower()
        sent = remove_quote(sent)
        sent = st.stem(sent)

        for elem in elements:
            elem = elem.lower()
            if elem == sent:
                data[KEY_PREDICTED_UI_ELEMENTS].append(elem)


    return data


if __name__ == '__main__':

    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v1_16_jun.csv'
    version = 1
    lst1 = process_data(fileloc, version)

    fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v2_16_jun.csv'
    version = 2
    lst2 = process_data(fileloc, version)

    for item in lst1 + lst2:
        detect(item)


