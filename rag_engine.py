import os

class SustainabilityRAG:

    def __init__(self):
        self.documents = {}
        self.load_documents()

    def load_documents(self):
        folder = "knowledge"

        for file in os.listdir(folder):
            if file.endswith(".txt"):
                with open(
                    os.path.join(folder, file),
                    "r",
                    encoding="utf-8"
                ) as f:
                    self.documents[file] = f.read()

    def retrieve(self, question):

        question = question.lower()

        if "water" in question or "leak" in question:
            return self.documents.get("water.txt", "")

        elif (
            "energy" in question
            or "electricity" in question
            or "power" in question
        ):
            return self.documents.get("energy.txt", "")

        elif (
            "waste" in question
            or "garbage" in question
            or "recycle" in question
        ):
            return self.documents.get("waste.txt", "")

        return self.documents.get("sdg.txt", "")