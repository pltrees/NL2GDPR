from helper.constant import *
import csv
import json


def read_csv(fileloc):
    rows = []
    with open(fileloc) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            rows.append(row)
    return rows

def write_to_json(data, fileloc):
    # Writing to sample.json
    with open(fileloc, "w") as p:
        json.dump(data, p, indent=2)


def write_to_txt(data, fileloc, mode):
    f = open(fileloc, mode)
    f.write(data)
    f.close()

def read_from_txt(fileloc):
    with open(fileloc, 'r') as myfile:
        data = myfile.read()
    return data


def read_from_json(fileloc):
    # read file
    with open(fileloc, 'r') as myfile:
        data = myfile.read()

    # parse file
    obj = json.loads(data)

    return obj
