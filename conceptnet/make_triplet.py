import re
import re
import json
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

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
reObj = re.compile(r'''/a/\[/r/(?:.+/)?([\w'.]+)/,/c/en/([\w'.]+)/(?:.+/)?,/c/en/([\w'.]+)/''')

relations = {
    'Antonym': 'Antonym',
    'DistinctFrom': 'Distinct From',
    'EtymologicallyRelatedTo': 'Etymologically Related To',
    'LocatedNear': 'Located Near',
    'RelatedTo': 'Related To',
    'SimilarTo': 'Similar To',
    'Synonym': 'Synonym',
    'AtLocation': 'At Location',
    'CapableOf': 'Capable Of',
    'Causes': 'Causes',
    'CausesDesire': 'Causes Desire',
    'CreatedBy': 'Created By',
    'DefinedAs': 'Defined As',
    'DerivedFrom': 'Derived From',
    'Desires': 'Desires',
    'NotDesires': 'Not Desires',
    'Entails': 'Entails',
    'ExternalURL': 'External URL',
    'FormOf': 'Form Of',
    'HasA': 'Has A',
    'HasContext': 'Has Context',
    'HasSubevent': 'Has Subevent',
    'HasFirstSubevent': 'Has First Subevent',
    'HasLastSubevent': 'Has Last Subevent',
    'HasPrerequisite': 'Has Prerequisite',
    'HasProperty': 'Has Property',
    'InstanceOf': 'Instance Of',
    'IsA': 'Is A',
    'MadeOf': 'Made Of',
    'MannerOf': 'Manner Of',
    'MotivatedByGoal': 'Motivated By Goal',
    'ObstructedBy': 'Obstructed By',
    'PartOf': 'Part Of',
    'ReceivesAction': 'Receives Action',
    'SenseOf': 'Sense Of',
    'SymbolOf': 'Symbol Of',
    'UsedFor': 'Used For',
}


# TYPE = 'brief'
TYPE = 'english'

processed, cnt = 0, 0
with open(TYPE + '.csv', 'r', encoding='utf-8') as in_file, \
        open(TYPE + '_triplet.txt', 'w', encoding='utf-8') as out_file:
    # words = set()
    try:
        while True:
            line = in_file.readline()
            # print(line)
            if not line: break
            cnt += 1

            matchObj = reObj.match(line)

            if matchObj:
                # print(line)x
                tokens = list(matchObj.groups())

                tokens = [regularize_word(tokens[1]), relations.get(tokens[0], tokens[0]), regularize_word(tokens[2])]

                print(' '.join(list(filter(lambda z: z!='', tokens))), file=out_file)

                processed += 1
            else:
                # print(line)
                pass

            if cnt % 10000 == 0:
                print('\r{:<10d} / {}'.format(processed, cnt), end='')
    except KeyError:
        print('line number {}: {}'.format(cnt, line))
        assert False

    '''words = list(words)
    words.sort()
    print(words, file=out_file)'''

print('\nTotal:', cnt)
