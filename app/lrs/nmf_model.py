from typing import Any

from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from .base_model import BaseModel


class NMFModel(BaseModel):
    def set_vectorizer(self, max_df: float, min_df: float, max_features: int) -> Any:
        self.vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df,
                                          max_features=max_features,
                                          stop_words=self.stop_list)
        return self.vectorizer

    def train(self, n_components: int, n_words: int, random_state: int,
              alpha: float, l1_ratio: float) -> None:
        tfidf = self.vectorize()

        self.trained_model = NMF(n_components=n_components,
                                 random_state=random_state,
                                 alpha=alpha,
                                 l1_ratio=l1_ratio).fit(tfidf)

        # Create Document - Topic Matrix
        model_output = self.trained_model.fit_transform(tfidf)

        self._set_model_attributes(model_output, n_components, n_words)

