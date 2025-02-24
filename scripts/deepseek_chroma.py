# test_chroma.py mit deepseek-embedding, das heisst die vektoren werden nicht wie standartmässig mit der chromadb erstellt sondern mit deepseek

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import subprocess
import json


# ------- FILES für die Geschichten --------
story1 = "".join(open("/home/zoe/Projects/DeepSeek/datasets/story1.txt", "r").readlines()) # das macht eine liste wo jedes element einen string ist also eine zeile
story2 = open("/home/zoe/Projects/DeepSeek/datasets/story2.txt", "r").readlines()
story3 = open("/home/zoe/Projects/DeepSeek/datasets/story3.txt", "r").readlines()

story_files = [story1, story2, story2]


# ------- VEKTOREN mit deepseek generieren -------
class MyEmbeddingFunction(MyEmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        return embeddings


def create_vectors_deepseek(text: str):
    # Aufruf von ollama mit dem DeepSeek-Modell, um den Text in einen Vektor umzuwandeln
    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:8b", "--input", text],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
    )
    print(result)

# Beispielaufruf
text = "Dies ist ein Beispieltext, den wir in einen Vektor umwandeln möchten."
vector = create_vectors_deepseek(story1)
print(f"Vektor: {vector}")