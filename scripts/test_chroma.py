# ohne embedding

import chromadb

# ------- FILES --------
story1 = open("/home/zoe/Projects/DeepSeek/datasets/story1.txt", "r").readlines() # das macht eine liste wo jedes element einen string ist also eine zeile
story2 = open("/home/zoe/Projects/DeepSeek/datasets/story2.txt", "r").readlines()
story3 = open("/home/zoe/Projects/DeepSeek/datasets/story3.txt", "r").readlines()

story_files = [story1, story2, story2]

# ------- CREATE -------

# Set up a client
client = chromadb.Client()

# Create collection
collection = client.create_collection("Geschichten")

# Fügt Geschichten ohne manuelle Vektoren hinzu
for i, story in enumerate(story_files, start=1):
    full_text = "".join(story)

    collection.add(
        documents=[full_text],
        metadatas=[  # Ein Metadaten-Objekt pro Dokument
            {"title": "".join(story[:1])}  # Titel aus der ersten Zeile
        ],
        ids=[f"{i}"],  # ID für das Dokument
    )

# ------- QUERY-ABFRAGEN -------

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["Wie heisst der Rock Frosch?"],  # Suchanfrage
    n_results=2,  # Wie viele ähnliche Ergebnisse zurückgeben
)

print(results)
