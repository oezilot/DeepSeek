'''
was macht das skript:
dieses skript füllt die chromadb mit den deepseek embeddings von gewissen daten

argumente:
- model, tokenizer, vector-embedingfuntkion, daten um in die datenbank zu tun
'''

import sys
sys.path.append("/home/zoe/Projects/DeepSeek/scripts")

import chromadb

from embedding import string_to_tensor # diese funktion kann mithilfe des models und dem tokenizer aus strings einen vektor machen
import run # dieses file lässt das model laufen und importiet den tokenizer, das modell als modul (run.modulname um es zu benutzen)


# ------- FILES für die Geschichten --------
story_paths = [
    "/home/zoe/Projects/DeepSeek/datasets/story1.txt",
    "/home/zoe/Projects/DeepSeek/datasets/story2.txt",
    "/home/zoe/Projects/DeepSeek/datasets/story3.txt"
]

stories = []
story_titles = []
story_texts = []

for path in story_paths:
    with open(path, "r") as file:
        lines = file.readlines()
        story_titles.append(lines[0])  # Erster Satz als Titel
        story_texts.append("".join(lines[1:]))  # Restlicher Text als Inhalt
        stories.append("".join(lines))  # Gesamter Text

# ------- Vektorumwandlung der Textfiles mit deepseek-embedding --------
# das passiert dann direkt wenn man die daten in die datenbank schreibt!

# ------- ChromaDB füllen/erstellen --------
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten") # hier muss man name, metadaten, embeddingfunktion angeben

# Prüfen, ob bereits Daten vorhanden sind
if collection.count() == 0:
    collection.add(
        ids=["story1", "story2", "story3"],
        embeddings=[string_to_tensor(text, run.model, run.tokenizer).mean(dim=1).squeeze().tolist() for text in stories], # wenn man die default emedding macht nutzt man die documents
        metadatas=[{"title": title, "content": text} for title, text in zip(story_titles, story_texts)] # optional und für filtering geacht
    )
    print("✅ ChromaDB erfolgreich mit Geschichten gefüllt!")
else:
    print("🔹 ChromaDB ist bereits gefüllt, keine neuen Daten hinzugefügt.")


'''
fragen:
- in welcher form müssen die vektoren sein die in die datenbank eingebracht werden? eine liste oder liste von listen oder tensoren?
'''