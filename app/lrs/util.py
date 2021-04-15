import os
import re
import string

import gensim
import numpy as np
import pandas as pd
import textacy
from spacy.language import Language
from textacy import preprocessing


def remove_dollar_sign(text):
    '''
    While drawing title count distribution, mathplotlib throws an error.
    Because some titles have dollar sign('$'). This method is used to clear the sign.
    '''

    text = str(text).replace('$', '\$')
    return text


def clean_text(text):
    '''
    Eliminates links, non alphanumerics, and punctuation.
    Returns lower case text.
    '''

    # Convert to string
    text = str(text)
    # Remove non-ascii
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Remove links
    text = re.sub('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', '', text)
    # Remove E-Mail addresses
    text = re.sub(r'\b[a-z]+@[a-z]+\b', r'', str(text))
    # Remove non-alphanumerics
    text = re.sub('\w*\d\w*', ' ', text)
    # Remove punctuation and lowercase
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text.lower())
    # Remove newline characters
    text = re.sub("\n", r' ', text)
    # Remove text in square brackets
    text = re.sub(r'\[.*?\]', '', text)
    # Remove words containing numbers
    text = re.sub(r'\w*\d\w*', '', text)
    # https://textacy.readthedocs.io/en/0.10.1/_modules/textacy/preprocessing/normalize.html
    text = textacy.preprocessing.normalize.normalize_whitespace(str(text))
    # replace words with less than 2 characters
    text = re.sub(r'\b[a-z]{1,2}\b', r'', str(text))

    return text


def replace_text(text, replacement_texts):
    pattern = re.compile("|".join([re.escape(i) for i in replacement_texts]))
    text = pattern.sub(lambda m: '', str(text))
    return text


def lemmatizer(text, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    sent = []
    doc = nlp(text)
    #  for word in doc:
    #    sent.append(word.lemma_)
    sent = [token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]

    return " ".join(sent)


# Lemmatization, remove pronouns.
def lemmatization(texts, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        texts_out.append(lemmatizer(" ".join(sent), nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']))
    return texts_out


def remove_stopwords(text, stop_list):
    clean_text = []
    for word in text.split(' '):
        if word not in stop_list and (len(word) > 2):
            clean_text.append(word)

    return ' '.join(clean_text)


def combine_authors(author_list):
    if isinstance(author_list, list):
        return ', '.join(author_list)

    return author_list


def display_topics(model, feature_names, no_top_words, no_top_topics, topic_names=None):
    count = 0
    for ix, topic in enumerate(model.components_):
        if count == no_top_topics:
            break
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", (ix + 1))
        else:
            print("\nTopic: '", topic_names[ix], "'")
        print(", ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        count += 1


def word_count(text):
    return sum([i.strip(string.punctuation).isalpha() for i in text.split()])


def get_file_name(file_path):
    f = os.path.basename(file_path)
    return f.replace('.pdf', '')


def compute_dists(top_vec, topic_array, norms):
    '''
    Returns cosine distances for top_vec compared to every article
    '''
    dots = np.matmul(topic_array, top_vec)
    input_norm = np.linalg.norm(top_vec)
    co_dists = dots / (input_norm * norms)
    return co_dists


def produce_rec_top_n(top_vec, topic_array, doc_topic_df, norms, n=5) -> pd.DataFrame:
    co_dists = compute_dists(top_vec, topic_array, norms)
    index_top_n = np.argpartition(co_dists, -n)[-n:]
    index_top_n = index_top_n[np.argsort(-co_dists[index_top_n])]

    return doc_topic_df.loc[index_top_n]


def sent_to_words(sentences):
    for sentence in sentences:
        yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))


def remove_non_english_sent(nlp: Language, text: str) -> str:
    doc = nlp(text)
    return ' '.join([sent.text for sent in doc.sents if sent._.language["language"] == 'en'])


def pre_process_text(text, REPLACED_WORDS, stop_list, nlp):
    # Clean
    for i in range(len(text)):
        text[i] = clean_text(text[i])

    # Remove Non-English sentences
    for i in range(len(text)):
        text[i] = remove_non_english_sent(nlp, text[i])

    for i in range(len(text)):
        text[i] = replace_text(text[i], REPLACED_WORDS)
    for i in range(len(text)):
        text[i] = clean_text(text[i])

    # Remove stopwords topic_array
    for i in range(len(text)):
        text[i] = remove_stopwords(text[i], stop_list)

    # Clean with simple_preprocess
    mytext_2 = list(sent_to_words(text))

    # Lemmatize
    mytext_3 = lemmatization(mytext_2, nlp, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    return mytext_3


# Methods Used Only on Training
def accuracy_n(file_path: str, text: str, model, top_n: [int] = [1]):
    topics, topic_probability_scores = model.predict_topic([text])

    recs = produce_rec_top_n(topic_probability_scores.flatten(),
                             model.topic_array,
                             model.doc_topic,
                             model.norms, max(top_n))

    existence = []

    for n in top_n:
        if recs['file_path'].head(n).str.contains(get_file_name(file_path)).any():
            existence.append(1)
        else:
            existence.append(0)

    return pd.Series(existence)


def calculate_accuracy_score_for_each_paper(input_data: pd.DataFrame, model, top_n: [int] = [1, 5, 10, 20, 100]):
    col_acc_n = ['acc_top_' + str(n) for n in top_n]
    input_data[col_acc_n] = input_data \
        .parallel_apply(lambda x: accuracy_n(x['file_path'], x['page_1'], model, top_n), axis=1)

    for n in top_n:
        print('Top-' + str(n) + ' Score:' + str(
            input_data['acc_top_' + str(n)].sum() / input_data['acc_top_' + str(n)].count()))
