import pandas as pd
import pickle5 as pickle

from app.lrs.base_model import BaseModel

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import en_core_web_sm

nlp = en_core_web_sm.load()  # https://spacy.io/usage/models#production
#https://pypi.org/project/spacy-langdetect/
from spacy_langdetect import LanguageDetector
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

MODEL_PATH = 'app/models/'
REPLACED_WORDS = pickle.load(open(MODEL_PATH + "replaced_words.pkl", "rb"))
stop_list = pickle.load(open(MODEL_PATH + "stop_list.pkl", "rb"))

ENGINE_TYPES = ['LDA', 'LDA', 'NMF', 'NMF']
ENGINE_VERSIONS = ['model_12_content_3_topic_80_20',
                   'model_12_content_10_topic_80_20',
                   'nmf_model_13_content_3_topic_80_20',
                   'nmf_model_13_content_10_topic_80_20']


# Utility functions
def make_suggestions(TAR_6, engine):
    # P R E D I C T I O N
    norms = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__norms.pkl", "rb"))
    topic_array = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__topic_array.pkl", "rb"))
    df_topic_keywords = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__df_topic_keywords.pkl", "rb"))
    doc_topic_df = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__doc_topic_df.pkl", "rb"))
    lda_model = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__topic_model.pkl", "rb"))
    count_vectorizer = pickle.load(open(MODEL_PATH + ENGINE_VERSIONS[engine] + "/model__vectorizer.pkl", "rb"))

    model = BaseModel(REPLACED_WORDS, stop_list, nlp)
    model.load_pretrained(norms, topic_array, df_topic_keywords, doc_topic_df, lda_model, count_vectorizer)

    return model.recommend(TAR_6)
