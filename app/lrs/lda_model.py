from typing import Any

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from .base_model import BaseModel


class LDAModel(BaseModel):

    def set_vectorizer(self, max_df: float, min_df: float, max_features: int) -> Any:
        self.vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df,
                                          max_features=max_features,
                                          stop_words=self.stop_list)
        return self.vectorizer

    def train(self, n_components: int, n_words: int, n_jobs: int = None) -> None:
        data_vectorized = self.vectorize()

        self.trained_model = LatentDirichletAllocation(n_components=n_components,  # Number of topics
                                                       learning_method='online',
                                                       random_state=0,
                                                       n_jobs=n_jobs  # Use all available CPUs
                                                       )

        # Create Document - Topic Matrix
        model_output = self.trained_model.fit_transform(data_vectorized)

        self._set_model_attributes(model_output, n_components, n_words)


