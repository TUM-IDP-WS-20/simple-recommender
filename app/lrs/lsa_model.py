from typing import Any

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from .base_model import BaseModel


class LSAModel(BaseModel):

    def set_vectorizer(self, max_df: float, min_df: float, max_features: int) -> Any:
        self.vectorizer = TfidfVectorizer(stop_words=self.stop_list,
                                          max_df=max_df,
                                          min_df=min_df,
                                          ngram_range=(1, 1),
                                          max_features=max_features)
        return self.vectorizer

    def train(self, n_components: int, n_words: int, n_iter: int = 5,
              algorithm: str = 'randomized', random_state: int = None) -> None:
        data_vectorized = self.vectorize()

        self.trained_model = TruncatedSVD(n_components=n_components,
                                          n_iter=n_iter,
                                          algorithm=algorithm,
                                          random_state=random_state)

        # Create Document - Topic Matrix
        model_output = self.trained_model.fit_transform(data_vectorized)

        self._set_model_attributes(model_output, n_components, n_words)
