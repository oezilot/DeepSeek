import chromadb
from deepseek_embedding import string_to_tensor

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
story_vectors = [string_to_tensor(text).mean(dim=1).squeeze().tolist() for text in stories]

# ------- ChromaDB füllen --------
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten")

# Prüfen, ob bereits Daten vorhanden sind
if collection.count() == 0:
    collection.add(
        ids=["story1", "story2", "story3"],
        embeddings=story_vectors,
        metadatas=[{"title": title, "content": text} for title, text in zip(story_titles, story_texts)]
    )
    print("✅ ChromaDB erfolgreich mit Geschichten gefüllt!")
else:
    print("🔹 ChromaDB ist bereits gefüllt, keine neuen Daten hinzugefügt.")