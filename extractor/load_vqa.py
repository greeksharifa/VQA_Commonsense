import json
import pandas as pd

'''
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False, default='vqa')
parser.add_argument('--name', type=str, required=True)
args = parser.parse_args()

'''
filenames = [
    'minival',
    'nominival',
    'test',
    'train'
]

x = False

for name in filenames:
    if x:
        break
    filename = "../data/vqa/{}.json".format(name)
    print('filename:', filename)

    dataset = pd.read_json(filename)

    # dataset = dataset.loc[:, ['question_id', 'sent']]







    x = True
    # print(dataset)