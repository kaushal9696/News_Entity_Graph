import string
from itertools import combinations
import pandas as pd
from flair.data import Sentence
from flair.models import SequenceTagger
from nltk import tokenize
import re

DFrame_GOcheck = pd.DataFrame()
DFrame_ImLinks = pd.DataFrame()
df = pd.read_csv('Articles_News.csv', skip_blank_lines=True)
LOAD_Tagger = SequenceTagger.load('ner')


def I_am_Data(Data_1):
    DFrame_Entities = []
    DFrame_Types = []

    Data_1 = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", Data_1)
    Data_1 = re.sub(r"\d+", "", Data_1)

    Start_Text = tokenize.sent_tokenize(Data_1)
    Start_Text = [Sentence(sent) for sent in Start_Text]

    for predict_me in Start_Text:
        LOAD_Tagger.predict(predict_me)

    Im_Dict = [Start_Text.to_dict(tag_type='ner') for Start_Text in Start_Text]

    for sent_dict in Im_Dict:
        DFrame_Entities.extend([entity['text'] for entity in sent_dict['entities']])
        DFrame_Types.extend(str(entity['labels'][-1]) for entity in sent_dict['entities'])
    try:
        DFrame_GOcheck = pd.DataFrame(data={'entity': DFrame_Entities, 'type': DFrame_Types})
        DFrame_GOcheck = DFrame_GOcheck[DFrame_GOcheck.type.str.match('(PER.*)|(ORG.*)')]
        DFrame_GOcheck = DFrame_GOcheck[DFrame_GOcheck['entity'].map(lambda x: isinstance(x, str))]
        DFrame_GOcheck['entity'] = DFrame_GOcheck['entity'].map(
            lambda x: x.translate(str.maketrans('', '', string.punctuation)))
        DFrame_GOcheck['entity'] = DFrame_GOcheck.apply(
            lambda x: x['entity'].split(' ')[len(x['entity'].split(' ')) - 1] if x['type'] == 'PER' else x['entity'],
            axis=1)
        DFrame_GOcheck = DFrame_GOcheck.drop_duplicates().sort_values('entity')
        Combinations = list(combinations(DFrame_GOcheck['entity'], 2))
        DFrame_ImLinks = pd.DataFrame(data=Combinations, columns=['from', 'to'])
        return DFrame_GOcheck, DFrame_ImLinks

    except:
        pass


for content in df['content']:
    try:
        GO_Temp1, Link_Temp2 = I_am_Data(content)
        DFrame_GOcheck = DFrame_GOcheck.append(GO_Temp1)
        DFrame_ImLinks = DFrame_ImLinks.append(Link_Temp2)

    except:
        continue

DFrame_GOcheck.to_csv('Entities_ALL.csv', index=False)
DFrame_ImLinks.to_csv('LinkOneTOone.csv', index=False)
