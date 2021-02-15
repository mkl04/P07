#
# Copyright 201-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import numpy as np
import pandas as pd

from bm25 import BM25
import unicodedata
import six
from nltk import word_tokenize

from transformers import pipeline

dfx = pd.read_csv('data/noticias.csv')
model_name = "mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
model = pipeline('question-answering', model=model_name, tokenizer=model_name)

def get_opening_message():
    '''The variable starting message.'''
    return f"Mande una pregunta por favor"

def numbered_print_list(lst):
    '''Display strings in a numbered list.'''
    final = ""
    for i, s in enumerate(lst):
        final += str(i+1) + '. ' + s + "\n"
    return final

def normalize_terms(terms):
    return [remove_diacritics(term).lower() for term in terms]

def remove_diacritics(text, encoding='utf8'):
    nfkd_form = unicodedata.normalize('NFKD', to_unicode(text, encoding))
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode(encoding)

def to_unicode(text, encoding='utf8'):
    if isinstance(text, six.text_type):
        return text
    return text.decode(encoding)

def do_bm25(query, df, best_n=3):

    query = normalize_terms(word_tokenize(query))
    text_lines_total = df.text.values

    text_lines_tokens = []
    for title in text_lines_total:
        
        title = re.sub(r'\W',' ', title) # matches any non-word character 
        title = re.sub(r'\s+',' ', title) # matches any whitespace character 
        title = title.replace('  ', ' ')
        title = title.replace('   ', ' ')

        tx_line = word_tokenize(title)
        text_lines_tokens.append(tx_line)
    
    news = [normalize_terms(sentence) for sentence in text_lines_tokens]
    bm25 = BM25(news)
    best_indexes = bm25.ranked(query, best_n)

    best_sentences = []
    for ind in best_indexes:
        sentence_found = text_lines_total[ind]
        best_sentences.append(sentence_found)

    return best_sentences


# state 1
def get_question(question):
    '''Ask user for the topic'''

    contexts = do_bm25(question, dfx, 3)
 
    best_score = 0
    for context in contexts:
        QA_input = {'question': question, 'context': context}
        res = model(QA_input)
        if res['score'] > best_score:
            best_score = res['score']
            best_answer = res['answer']

        print("score: ", res['score'])
        print("answer: ", res['answer'])
        print("==========")


    return "La respuesta es:  {}\nCon un porcentaje de {}% \n\nPuede realizar otra pregunta: ".format(best_answer, np.round(best_score*100), 1), 1


# state 5
def end(any_text):
    '''State that appears when the app is restarted'''
    return "restarting app...\n\n" + get_opening_message(), 1, {}

