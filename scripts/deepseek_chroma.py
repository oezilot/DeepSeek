import chromadb
from deepseek_embedding import string_to_tensor

# ------- FILES für die Geschichten --------
story1 = open("/home/zoe/Projects/DeepSeek/datasets/story1.txt", "r").readlines() # das macht eine liste wo jedes element einen string ist also eine zeile
story2 = open("/home/zoe/Projects/DeepSeek/datasets/story2.txt", "r").readlines()
story3 = open("/home/zoe/Projects/DeepSeek/datasets/story3.txt", "r").readlines()

story_files = ["".join(story1), "".join(story2), "".join(story3)]
story_titles = [story1[0], story2[0], story3[0]]
story_texts = ["".join(story1[1:]), "".join(story2[1:]), "".join(story3[1:])]


# ------- Vektorumwandlung der Textfiles mit deepseek-embedding --------
# für kleine texte muss man die texte nicht aufteilen in kleinere stücke
story_files = [string_to_tensor(file).mean(dim=1).squeeze().tolist() for file in story_files]


# ------- ChromaDB füllen --------
# Verbindung zur Chromadb
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")

collection = client.get_or_create_collection("Geschichten")

# die zusammengefassten vektoren müssen eine gewisse länge haben damit man diese in die datenbank einfügen kann (dimension = 4096 elemente pro vektor)
collection.add(
    ids=["story1", "story2", "story3"],  # Liste von IDs
    embeddings=[
        story_files[0],  # Erster Vektor für story1
        story_files[1],   # Zweiter Vektor für story2
        story_files[2]   # Zweiter Vektor für story3
    ],
    metadatas=[
        {"title": story_titles[0], "content": story_texts[0]},  # Metadaten für story1
        {"title": story_titles[1], "content": story_texts[1]},   # Metadaten für story2
        {"title": story_titles[2], "content": story_texts[2]}   # Metadaten für story3
    ]
)
'''
# Query/search 2 most similar results. You can also .get by id
query_results = collection.query(
    query_texts=["Wie heisst der Rock Frosch?"],  # Suchanfrage
    n_results=1,  # Wie viele ähnliche Ergebnisse zurückgeben
)
print(query_results)
'''