import chromadb
from deepseek_embedding import string_to_tensor

# Verbindung zur bestehenden ChromaDB-Datenbank
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten")

# Suchanfrage als Vektor umwandeln
query_text = "Wie heisst der Rock Frosch?"
query_vector = string_to_tensor(query_text).mean(dim=1).squeeze().tolist()

# Suche nach ähnlichen Einträgen
query_results = collection.query(
    query_embeddings=[query_vector],
    n_results=2  # Zwei ähnlichste Geschichten finden
)

# Ergebnis ausgeben
print("🔍 Suchergebnisse:", query_results)


'''
query-parameter:
- query_embeddings -> der wert der collection wessen vektor am nähsten dem input-promt ist (mit chromadb-builtin wäre hier query_texts oder so)
'''