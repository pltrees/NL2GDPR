from data_processor.preprocess import *
from nltk.stem.lancaster import LancasterStemmer



def pii_detector(sent):
    '''if we explore with OIA then it will help us to avoid event. For example, registration process wont be detected as noun. so it will help us to avoid FP'''
    '''
       UI Elements: [TextView, EditText, Button, ImageButton, ToggleButton, RadioButton, RadioGroup, CheckBox, AutoCompleteTextView, ProgressBar, Spinner, TimePicker, DatePicker, SeekBar, AlertDialog, Switch, RatingBar]
   **To learn more about UI elements, visit here: data-flair.training/blogs/android-ui-controls/.
   Events: [press, long pressed]
   **To learn more about events, visit here: developer.android.com/guide/topics/ui/ui-events.
   Resource: [image, text, video]
   Data: [username, firstname, lastname, name, email, mail, address, country, state, zipcode, city, county, age, location, birthdate, ipaddress]
       '''

    # elements = ['TextView', 'EditText', 'Button', 'ImageButton', 'ToggleButton', 'RadioButton', 'RadioGroup',
    #             'CheckBox', 'AutoCompleteTextView', 'ProgressBar', 'Spinner', 'TimePicker', 'DatePicker', 'SeekBar',
    #             'AlertDialog', 'Switch', 'switchbutton', 'RatingBar', 'Map', 'RadioButtonControl']

    elements = {

    'username': ['username', 'uname'],
    'firstname': ['firstname', 'fname'],
    'lastname' : ['lastname', 'lname'],
    'name':['name', 'fullname'],
    'email' : ['email', 'mail'],
    'address': ['address'],
    'country': ['country'],
    'state': ['state', 'st'],
    'zipcode': ['zipcode', 'zip'],
    'city': ['city'],
    'county': ['county'],
    'age': ['age'],
    'location': ['location', 'loc'],
    'birthdate': ['birthdate', 'bday', 'dob'],
    'ipaddress' : ['ipaddress', 'ip'],
    'password' : ['password', 'pass'],
    'userinformation' : ['userinformation']
    }


    # st = LancasterStemmer()

    lst = []

    # data = {}
    # data[KEY_SENT] = sent
    # data[KEY_PREDICTED_PII] = []

    # data[TAG_PAGE_NAME] = ""

    # if 'page' in token and iter > 0:
    #     data[TAG_PAGE_NAME] = tokens[iter - 1]


    tokens = sent.split(' ')

    for sent in tokens:
        sent = sent.lower()
        sent = remove_quote(sent)
        # sent = st.stem(sent)
        # print(sent)

        for key, vals in elements.items():
            for val in vals:
                val = val.lower()
                if val == sent:
                    lst.append(key)


    return lst

def test():

    sent = 'Each imagebutton could be clicked to show more userinformation'
    sent = "when you click the imagebutton of 'country', a 'radiobuttoncontrol' pops up, you can select the city where you are, and click the button of 'continue' to send the user's 'email' and 'password' to the server, and jump to 'registered successfully' page"
    detector = pii_detector(sent)
    print(detector)

if __name__ == '__main__':

    test()

    # fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v1_16_jun.csv'
    # version = 1
    # lst1 = process_data(fileloc, version)
    #
    # fileloc = '/home/faysal-gpu/code/intern/gdpr-code-generator/data/v2_16_jun.csv'
    # version = 2
    # lst2 = process_data(fileloc, version)



