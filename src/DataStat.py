import sys

# appending a path
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/')
from data_processor.read_write_data import *



def get_total_feature_number():
    data_list = get_label_data()

    track_dict = {}
    for data in data_list:
        feature = data['feat']
        if feature not in track_dict:
            track_dict[feature] = 0
        track_dict[feature] += 1

    total  = 0
    for k,v in track_dict.items():
        print(k, '->', v)
        total += v

    print("Total Feature=", len(track_dict))

if __name__ == '__main__':
    get_total_feature_number()