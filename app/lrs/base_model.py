from abc import abstractmethod
from typing import Any, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from spacy.language import Language

from .util import pre_process_text, produce_rec_top_n


class BaseModel:
    # External attributes
    words_to_replace: [str]
    stop_list: [str]
    nlp: Language

    # Technique Parameters
    norms: np.ndarray
    topic_array: np.ndarray
    topic_keywords: pd.DataFrame
    doc_topic: pd.DataFrame
    trained_model: Any
    vectorizer: Any

    df: pd.DataFrame
    columns: [str]
    data_column: str

    def __init__(self, words_to_replace: [str], stop_list: [str],
                 nlp: Language) -> None:
        self.words_to_replace = words_to_replace
        self.stop_list = stop_list
        self.nlp = nlp
        self.df = None
        self.vectorizer = None
        self.trained_model = None

    @abstractmethod
    def set_vectorizer(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def train(self, **kwargs) -> None:
        """
        Train model and set the following model attributes:
        norms: np.ndarray
        topic_array: np.ndarray
        topic_keywords: pd.DataFrame
        doc_topic: pd.DataFrame
        trained_model: Any
        vectorizer: Any
        """
        if self.df is None:
            raise Exception("Data should be loaded. Use 'model.load_data()' function to load data.")

    def vectorize(self) -> Any:
        if self.vectorizer is None:
            raise Exception("First set vectorizer using 'model.set_vectorizer()' function.")

        return self.vectorizer.fit_transform(self.df[self.data_column])

    def get_features(self) -> [str]:
        return self.vectorizer.get_feature_names()

    def load_data(self, df: pd.DataFrame, columns: [str], data_column: str):
        self.df = df
        self.columns = columns
        self.data_column = data_column

    def load_pretrained(self, norms: np.ndarray, topic_array: np.ndarray, topic_keywords: pd.DataFrame,
                        doc_topic: pd.DataFrame, trained_model: Any, vectorizer: Any):
        self.norms = norms
        self.topic_array = topic_array
        self.topic_keywords = topic_keywords
        self.doc_topic = doc_topic
        self.trained_model = trained_model
        self.vectorizer = vectorizer

    def predict_topic(self, text: [str]) -> Tuple[np.ndarray, np.ndarray]:
        if self.trained_model is None:
            raise Exception("There is no trained model. Either train model with 'model.train()' "
                            "function or load pretrained model with 'model.load_pretrained()' function")

        # Clean data
        processed_text = pre_process_text(text, self.words_to_replace,
                                          self.stop_list, self.nlp)
        # Transform
        transformed_data = self.vectorizer.transform(processed_text)

        # Calculate Topic Probability Score
        topic_probability_scores = self.trained_model.transform(transformed_data)

        # Find the topic that has highest probability
        topics = self.topic_keywords.iloc[np.argmax(topic_probability_scores), :].values.tolist()

        return topics, topic_probability_scores

    def recommend(self, text: str) -> pd.DataFrame:
        topics, prob_scores = self.predict_topic([text])

        recs = produce_rec_top_n(prob_scores.flatten(), self.topic_array, self.doc_topic, self.norms)

        topic_columns = ['Topic ' + str(i) for i in range(1, self.topic_keywords.shape[0] + 1)]
        recs['similarity'] = cosine_similarity(recs[topic_columns].values, prob_scores)

        return recs

    def show_topics(self, n_words: int) -> [np.ndarray]:
        keywords = np.array(self.vectorizer.get_feature_names())
        topic_keywords = []
        for topic_weights in self.trained_model.components_:
            top_keyword_locs = (-topic_weights).argsort()[:n_words]
            topic_keywords.append(keywords.take(top_keyword_locs))
        return topic_keywords

    def _set_model_attributes(self, model_output, n_components, n_words):
        topic_names = ["Topic {}".format(i + 1) for i in range(n_components)]

        topic_keywords = self.show_topics(n_words)
        self.topic_keywords = pd.DataFrame(topic_keywords)
        self.topic_keywords.columns = ['Word ' + str(i) for i in range(self.topic_keywords.shape[1])]
        self.topic_keywords.index = ['Topic ' + str(i) for i in range(self.topic_keywords.shape[0])]
        self.topic_keywords['topic_theme'] = topic_names
        self.topic_keywords.set_index('topic_theme', inplace=True)
        # column names
        topic_columns = self.topic_keywords.T.columns
        # index names
        doc_names = ["Doc" + str(i) for i in range(len(self.df))]
        # Make the pandas dataframe
        df_document_topic = pd.DataFrame(np.round(model_output, 2), columns=topic_columns, index=doc_names)

        # Get dominant topic for each document
        dominant_topic = np.argmax(df_document_topic.values, axis=1)
        df_document_topic['dominant_topic'] = dominant_topic

        df_document_topic.reset_index(inplace=True)
        df_sent_topic = pd.merge(self.df, df_document_topic, left_index=True, right_index=True)
        df_sent_topic.drop('index', axis=1, inplace=True)

        ###################################

        topic_sum = pd.DataFrame(np.sum(model_output, axis=1))

        column_names = self.columns + topic_names + ['sum']

        # Turn our docs_nmf array into a data frame
        self.doc_topic = pd.DataFrame(data=model_output)

        # Merge all of our article metadata and name columns
        self.doc_topic = pd.concat([self.df,
                                    self.doc_topic, topic_sum], axis=1)
        self.doc_topic.columns = column_names

        # Remove articles with topic sum = 0, then drop sum column
        self.doc_topic = self.doc_topic[self.doc_topic['sum'] != 0]
        self.doc_topic.drop(columns='sum', inplace=True)

        # Reset index then save
        self.doc_topic.reset_index(drop=True, inplace=True)
        # doc_topic_df.to_pickle('counter_vectorizer_LDA_8topics_stemmed.pkl')

        self.topic_array = np.array(self.doc_topic[topic_names])
        self.norms = np.linalg.norm(self.topic_array, axis=1)
