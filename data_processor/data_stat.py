from data_processor.read_write_data import *

def get_total_feature_stat(datalist):
    feat_dict = {}
    for data in datalist:
        if data[KEY_FEAT] not in feat_dict:
            feat_dict[data[KEY_FEAT]] = 0
        feat_dict[data[KEY_FEAT]] += 1

    total = 0
    for k,v in feat_dict.items():
        print(k, '->', v)

        total += v

    print(total)

if __name__ == '__main__':
    data_list = get_label_data()
    get_total_feature_stat(data_list)