import os
import re
import string
import pandas as pd
import numpy as np
import pickle5 as pickle
import gensim
from textacy import preprocessing
import textacy
from sklearn.metrics.pairwise import cosine_similarity
import gc

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import en_core_web_sm

nlp = en_core_web_sm.load()  # https://spacy.io/usage/models#production

MODEL_PATH = 'app/models/'
REPLACED_WORDS = pickle.load(open(MODEL_PATH + "replaced_words.pkl", "rb"))
stop_list = pickle.load(open(MODEL_PATH + "stop_list.pkl", "rb"))

ENGINE_TYPES = ['LDA', 'LDA', 'NMF', 'NMF']
ENGINE_VERSIONS = ['model_12_content_3_topic_80_20',
                   'model_12_content_10_topic_80_20',
                   'nmf_model_13_content_3_topic_80_20',
                   'nmf_model_13_content_10_topic_80_20']


# Utility functions
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


def replace_text(text, replacement_texts=REPLACED_WORDS):
    pattern = re.compile("|".join([re.escape(i) for i in replacement_texts]))
    text = pattern.sub(lambda m: '', str(text))
    return text


def lemmatizer(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    sent = []
    doc = nlp(text)
    #  for word in doc:
    #    sent.append(word.lemma_)
    sent = [token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]

    return " ".join(sent)


# Lemmatization, remove pronouns.
def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        texts_out.append(lemmatizer(" ".join(sent), allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']))
    return texts_out


def remove_stopwords(text):
    clean_text = []
    for word in text.split(' '):
        if word not in stop_list and (len(word) > 2):
            clean_text.append(word)

    return ' '.join(clean_text)


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


def make_suggestions(TAR_6, engine):
    def compute_dists(top_vec, topic_array, norms):
        '''
        Returns cosine distances for top_vec compared to every article
        '''
        dots = np.matmul(topic_array, top_vec)
        input_norm = np.linalg.norm(top_vec)
        co_dists = dots / (input_norm * norms)
        return co_dists

    def produce_rec_top_n(top_vec, topic_array, doc_topic_df, norms, n=5):
        co_dists = compute_dists(top_vec, topic_array, norms)
        index_top_n = np.argpartition(co_dists, -n)[-n:]
        index_top_n = index_top_n[np.argsort(-co_dists[index_top_n])]
        return doc_topic_df.loc[index_top_n]

    def sent_to_words(sentences):
        for sentence in sentences:
            yield (gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def predict_topic(text, lda_model, count_vectorizer, df_topic_keywords, nlp=nlp):

        # Clean
        for i in range(len(text)):
            text[i] = clean_text(text[i])

        for i in range(len(text)):
            text[i] = replace_text(text[i])
        for i in range(len(text)):
            text[i] = clean_text(text[i])

        # Remove stopwords topic_array
        for i in range(len(text)):
            text[i] = remove_stopwords(text[i])

        # Clean with simple_preprocess
        mytext_2 = list(sent_to_words(text))

        # Lemmatize
        mytext_3 = lemmatization(mytext_2, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

        # stemming is skipped !!!
        # mytext_3_1 = []
        # for t in mytext_3:
        #  mytext_3_1.append(stem_text(t))

        # Vectorize transform
        mytext_4 = count_vectorizer.transform(mytext_3)

        # print('Count vectorizer of transformed text: {}'.format(mytext_4.shape))
        # print('Vectorized data {}'.format(data_vectorized.shape))
        # print('First 100 Feature names:')
        # print(count_vectorizer.get_feature_names()[:100])
        # print('')

        # LDA Transform
        topic_probability_scores = lda_model.transform(mytext_4)
        topic = df_topic_keywords.iloc[np.argmax(topic_probability_scores), :].values.tolist()
        return topic, topic_probability_scores

    # P R E D I C T I O N
    norms = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__norms.pkl", "rb"))
    topic_array = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__topic_array.pkl", "rb"))
    df_topic_keywords = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__df_topic_keywords.pkl", "rb"))
    doc_topic_df = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__doc_topic_df.pkl", "rb"))
    lda_model = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__topic_model.pkl", "rb"))
    count_vectorizer = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__vectorizer.pkl", "rb"))

    topic, prob_scores = predict_topic([TAR_6], lda_model, count_vectorizer, df_topic_keywords)
    """
    print('topic')
    print(topic)
    print('')
    print('prob_scores')
    print(prob_scores[0])
    print("shape of prob_scores: {}".format(prob_scores[0].shape))
    print('')

    print("Try to make recommendation. Inputs:")
    print("- prob_scores")
    print("- topic_array: {} prob. distribution of topics for each document that is calculated by LDA".format(
        topic_array.shape))
    print("- doc_topic_df: {} that is actually output of the LDA but combined with file_path, etc.".format(
        doc_topic_df.shape))
    print('')
    print(doc_topic_df.columns)
    """

    recs = produce_rec_top_n(prob_scores.flatten(), topic_array, doc_topic_df, norms)

    topic_columns = ['Topic ' + str(i) for i in range(1, df_topic_keywords.shape[0] + 1)]
    recs['similarity'] = cosine_similarity(recs[topic_columns].values, prob_scores)

    del norms
    del topic_array
    del df_topic_keywords
    del doc_topic_df
    del lda_model
    del count_vectorizer
    del prob_scores
    del topic
    del topic_columns
    gc.collect()

    return recs
