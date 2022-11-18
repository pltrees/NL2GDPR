import pickle
import json
import sys
import argparse

import sys

# appending a path
sys.path.append('/home/faysal-gpu/code/intern/gdpr-code-generator/')
from data_processor.read_write_data import *


def postprocess_cluster(cluster_file_path, path):
    with open(cluster_file_path, 'rb') as f:
        predicted_cluters = pickle.load(f)

    with open(path, 'r') as f:
        samples = [json.loads(line) for line in f.readlines()]

    doc_id = 0

    lst = []

    for doc_key, clusters in predicted_cluters.items():
        assert samples[doc_id]['doc_key'] == doc_key
        print(doc_key)
        sentences = samples[doc_id]['sentences']
        words = samples[doc_id]['tokens']
        token = [tok for s in sentences for tok in s]
        subtokenmap = samples[doc_id]['subtoken_map']
        sentence_id = samples[doc_id]['sentence_map']
        doc_id += 1
        for c_id, c in enumerate(clusters):
            mention_strs = []
            mention_in_sentences = []
            for mention in c:
                mention_strs.append(' '.join(words[subtokenmap[mention[0]]:subtokenmap[mention[1]] + 1]))
                mention_in_sentences.append(sentence_id[mention[0]] + 1)

            info = f'doc {doc_key} cluster id {c_id}: {mention_strs} respectively in sentence {mention_in_sentences}'
            print(info)

            doc_dict = {}
            doc_dict['doc_index'] = doc_key
            doc_dict['c_id'] = c_id
            doc_dict['mention_strs'] = mention_strs
            doc_dict['mention_in_sentences'] = mention_in_sentences



            lst.append(doc_dict)

    write_to_json(lst, '/home/faysal-gpu/code/intern/gdpr-code-generator/src/coref/output/coref.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--cluster_file_path",
                        default="/home/faysal-gpu/code/intern/gdpr-code-generator/sota/coref_tool/conll-2012/data/output/spanbertlarge_coref_part.pkl",
                        type=str, help="predicted clusters pkl file")
    parser.add_argument("--data_path",
                        default="/home/faysal-gpu/code/intern/gdpr-code-generator/sota/coref_tool/conll-2012/data/output/english.512.jsonlines",
                        type=str, help="preprocessed json data path")

    args = parser.parse_args()
    postprocess_cluster(args.cluster_file_path, args.data_path)