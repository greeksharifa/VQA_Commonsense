from pprint import pprint
import re
from tqdm import tqdm
import json
import pandas as pd
from collections import Counter

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from load_paper import dataset_paper

stop_words = set(stopwords.words("english"))

filenames = [
    'minival',
    'nominival',
    'test',
    'train'
]

x = False


def regularize_word(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()

    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    ##Convert to list from string
    text = text.split()

    ##Stemming
    ps = PorterStemmer()
    # Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in stop_words]
    text = " ".join(text)

    return text


def triplet_to_word2row_idx():
    word2row_idx = dict()

    with open('../conceptnet/english_triplet.txt', 'r', encoding='utf-8') as in_file:
        comn_sents = in_file.readlines()
        for row_idx, line in enumerate(tqdm(comn_sents)):
            for word in line.strip().split(' '):
                if word not in word2row_idx:
                    word2row_idx[word] = set()
                word2row_idx[word].add(row_idx)

    print("comn_sents:")
    print(comn_sents[:20])

    return word2row_idx, comn_sents


for name in filenames:
    if x:
        break
    filename = "../data/vqa/{}.json".format(name)
    print('filename:', filename)

    vqa_dataset = json.load(open(filename, 'r', encoding='utf-8'))

    dataset = pd.read_json(filename)
    # dataset = dataset_paper
    print('len(dataset):', len(dataset))

    corpus = []
    for i in range(0, len(dataset)):
        # Remove punctuations
        text = regularize_word(dataset['sent'][i])

        corpus.append(text)

    cv = CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=10000, ngram_range=(1, 3))
    X = cv.fit_transform(corpus)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)
    # get feature names
    feature_names = cv.get_feature_names()

    word2row_idxs, comn_sents = triplet_to_word2row_idx()

    # fetch document for which keywords needs to be extracted
    # print('len(corpus):', len(corpus))

    qid2row_idxs = dict()

    for i, doc in enumerate(tqdm(corpus)):

        # generate tf-idf for the given document
        tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))


        def sort_coo(coo_matrix):
            tuples = zip(coo_matrix.col, coo_matrix.data)
            return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


        def extract_topn_from_vector(feature_names, sorted_items, topn=10):
            """get the feature names and tf-idf score of top n items"""

            # use only topn items from vector
            sorted_items = sorted_items[:topn]

            score_vals = []
            feature_vals = []

            # word index and corresponding tf-idf score
            for idx, score in sorted_items:
                # keep track of feature name and its corresponding score
                score_vals.append(round(score, 3))
                feature_vals.append(feature_names[idx])

            # create a tuples of feature,score
            # results = zip(feature_vals,score_vals)
            results = {}
            for idx in range(len(feature_vals)):
                results[feature_vals[idx]] = score_vals[idx]

            return results


        # sort the tf-idf vectors by descending order of scores
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        # extract only the top n; n here is 10
        keywords = extract_topn_from_vector(feature_names, sorted_items, 5)

        '''final_keywords = []

        for idx1, i_word in enumerate(keywords):
            included = False
            for idx2, j_word in enumerate(keywords):
                if idx1==idx2:
                    continue
                if i_word in j_word:
                    included = True
                    break
            if not included:
                final_keywords.append(i_word)'''
        '''now print the results
        print("\nSent:", dataset['sent'][i], sep='\n')
        print(doc)
        print("Keywords:", set(keywords.keys()))  # '|\t  \t|'.join(keywords), sep='\n')'''

        result_set = set()

        for key in set(keywords.keys()):
            row_idxs = word2row_idxs.get(key, set())
            result_set = result_set.union(row_idxs)

        #print('result_set:', len(result_set))
        qid2row_idxs[i] = list(result_set)

        try:
            comn_sent = comn_sents[next(iter(result_set))]
        except StopIteration:
            comn_sent = "nothing"

        vqa_dataset[i]["comn_sent"] = comn_sent.strip()

        '''with open('../data/vqa/comn_sents_' + name + '.json', 'a', encoding='utf-8') as fp:
            pprint(vqa_dataset[i], stream=fp)
            print(comn_sent, file=fp, end='')

        if i < 20:
            pprint(vqa_dataset[i], stream=open())'''


    with open('../data/vqa/comn_sents_' + name + '.json', 'w', encoding='utf-8') as fp:
    #    json.dump(qid2row_idxs, fp=fp)
        # json.dump(vqa_dataset, sort_keys=True, indent=4, fp=fp)
        json.dump(vqa_dataset, indent=4, fp=fp)

    # x = True
