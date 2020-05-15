import pandas as pd


dataset_paper = pd.read_csv('papers.csv')

dataset_paper = dataset_paper[dataset_paper['abstract'] != 'Abstract Missing'][['id', 'abstract']]
dataset_paper.rename(columns={'id': 'qid', 'abstract': 'sent'}, inplace=True)
# dataset['word_count'] = dataset['abstract'].apply(lambda x: len(str(x).split(" ")))

dataset_paper.reset_index(inplace=True)
