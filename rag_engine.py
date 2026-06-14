import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SustainabilityRAG:

    def __init__(self):

        self.documents = []

        self.load_documents()

        self.vectorizer = TfidfVectorizer()

        self.document_vectors = self.vectorizer.fit_transform(
            self.documents
        )

    def load_documents(self):

        folder = "knowledge"

        for file in os.listdir(folder):

            if file.endswith(".txt"):

                with open(
                    os.path.join(folder, file),
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.documents.append(
                        f.read()
                    )

    def retrieve(self, question):

        query_vector = self.vectorizer.transform(
            [question]
        )

        similarities = cosine_similarity(
            query_vector,
            self.document_vectors
        )

        best_match_index = similarities.argmax()

        return self.documents[
            best_match_index
        ]   