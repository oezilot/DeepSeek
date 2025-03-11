'''
dieses skript gibt die metadaten für den datenpunkt in der chromadb zurück welcher am nächsten zu einenm gewissen string liegt

link zur dokunetation: 
- https://docs.trychroma.com/docs/collections/create-get-delete
- https://cookbook.chromadb.dev/core/advanced/queries/
'''

import sys
sys.path.append("/home/zoe/Projects/DeepSeek/scripts")

import chromadb

from embedding import string_to_tensor
import run # dieses file lässt das model laufen und importiet den tokenizer, das modell als modul (run.modulname um es zu benutzen)


# Verbindung zur bestehenden ChromaDB-Datenbank
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten") # wenn man die cellection gettet oder kreiert muss man immer de embeddingfunktione angeben! -> client.get_collection(name="my_collection", embedding_function=emb_fn)

# Suchanfrage als Vektor umwandeln
query_text = "Prinz"
query_vector = string_to_tensor(query_text, run.model, run.tokenizer).mean(dim=1).squeeze().tolist()

# Suche nach ähnlichen Einträgen, zurück komt die gesamte collection mit den daten die am ähnlichsten sind
query_results = collection.query(
    query_embeddings=[query_vector], # man sucht in der datenbank den vektor welcher am ähnlichsten ist wie der query_vector
    n_results=1,  # Zwei ähnlichste Geschichten finden
    include = ["embeddings", "metadatas", "distances"]
)

# Ergebnis ausgeben
print("🔍 Suchergebnisse:", query_results)


'''
fragen:
- müsste man um die vektoren zu vergleichen nicht auch eine deepseek-algorithmus nehmen?
'''