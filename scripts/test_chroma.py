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
        metadatas=[  # Ein Metadaten-Objekt pro Dokument (????????????????????)
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



'''mein alter code der nicht geht weil ich zu viele metadaten habe
# ohne embedding

import chromadb

# ------- FILES --------
story1 = open("/home/zoe/Projects/DeepSeek/datasets/story1.txt", "r").readlines() # das macht eine liste wo jedes element einen string ist also eine zeile
story2 = open("/home/zoe/Projects/DeepSeek/datasets/story2.txt", "r").readlines()
story3 = open("/home/zoe/Projects/DeepSeek/datasets/story3.txt", "r").readlines()

story_files = [story1, story2, story2]


# ------- CREATE -------

# stup a client. clients interagieren mit der datenbank (erstellen, abfragen und bearbeiten von datensätzen) (persistent vs. inmemory)
client = chromadb.Client()

# Create collection, eine collection ist wie eine tabelle (get_collection, get_or_create_collection, delete_collection also available!)
collection = client.create_collection("Geschichten")

# die zeilen in die tabele hinzufügen -> jede zeile ist eine geschichte (die namen ids, metadatas, documents sind fest vorgegeben!)
# jedes element der lsten steht für den wert einer zeile listenname[x] => element der zeile x
# das document wird automatisch in einen voktor umgewandelt! wenn man seinen eigenen algorithmus verwenden will um vektoren zu erzeugen muss man dass mit embeddings tun und einem model welches man zuerst definieren muss und welches dann auch diese vektoren berechnet

# füge die erste geschichte hinzu
collection.add(
    documents=["".join(story1)], # dieser string wird dann in einen vektor umgewandelt
    metadatas=[
        {"title": "".join(story1[:1])}, 
        {"author": "Zoé Flumini"}, 
        {"text": "".join(story1[1:])}], 
    ids=[1], # unique for each doc
)
# füge die zweite geschichte hinzu
collection.add(
    documents=["".join(story2)], 
    metadatas=[
        {"title": "".join(story2[:1])},  
        {"author": "Anna Flumini"},
        {"text": "".join(story2[1:])},  
    ],
    ids=[2], 
)
# füge die dritte geschichte hinzu
collection.add(
    documents=["".join(story3)], 
    metadatas=[
        {"title": "".join(story3[:1])},  
        {"author": "ChatGPT"},
        {"text": "".join(story3[1:])},  
    ],
    ids=[3], 
)


# ------- QUERY-ABFRAGEN -------

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["Wie heisst der Rock Frosch?"], # das ist eine suchanfrage, es wird in der datenbank nach documents (vektoren!) gesucht die semantisch am ähnlichsten sind wie dieser input (nicht wortwörtlich!)
    n_results=2, # wie viele ähnlichte dokumente werden zurückgegeben?
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)
'''