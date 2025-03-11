'''
dieses skript generiert eine antwort zu einem promt. die argumente sind das model und der tokenizer und eine chomadatenbank die gefüllt ist
'''


#import sys
#sys.path.append("/home/zoe/Projects/DeepSeek/scripts")

import chromadb
import torch

#from embedding import string_to_tensor
#import run # dieses file lässt das model laufen und importiet den tokenizer, das modell als modul (run.modulname um es zu benutzen)



''' for testing
# Verbindung zur bestehenden ChromaDB-Datenbank
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten") # wenn man die cellection gettet oder kreiert muss man immer de embeddingfunktione angeben! -> client.get_collection(name="my_collection", embedding_function=emb_fn)

# Suchanfrage als Vektor umwandeln
query_text = "We heisst der Frosch?"
query_vector = string_to_tensor(query_text, run.model, run.tokenizer).mean(dim=1).squeeze().tolist()
'''

def find_chroma_match(query_vector, collection):

    # Suche nach ähnlichen Einträgen, zurück komt die gesamte collection mit den daten die am ähnlichsten sind
    query_results = collection.query(
        query_embeddings=[query_vector], # man sucht in der datenbank den vektor welcher am ähnlichsten ist wie der query_vector
        n_results=1,  # Zwei ähnlichste Geschichten finden
        include = ["embeddings", "metadatas", "distances"]
    )

    # Ergebnis ausgeben
    print("🔍 Suchergebnisse:", query_results)

    return query_results


def generate_response(query_text, model, tokenizer, query_results):

    # die relevanten informationen aus den query-resukts herausnehmen
    metadata = query_results["metadatas"][0][0] # das muss man machen weil der output eine liste von listen von dictonariey ist (die gesamte collection) aber nur ein einziges dictionary drin ist!
    title = metadata["title"]
    content = metadata["content"]

    # deepseek muss nun schlau auf die frage antworten mit den daten aus der chromadb
    messages = [
        {"role": "system", "content": "Du bist ein hilfreicher KI-Assistent, der Fragen anhand von Hintergrundwissen beantwortet."},
        {"role": "user", "content": f"Hier ist eine relevante Geschichte:\n\nTitel: {title}\n\nInhalt: {content}\n\nNutze diese Information, um die folgende Frage möglichst schön und ausführlich zu beantworten."},
        {"role": "user", "content": f"Frage: {query_text}"},
    ]

    # den promt für deepseek in tokenform bringen
    input_tokens = tokenizer.apply_chat_template(messages, return_tensors="pt").to(model.device) # den promt für deepseek in tokenform bringen

    # eine antwort generieren mit deepseek
    with torch.no_grad():
        output = model.generate(input_tokens, max_new_tokens=200)  # Antwort generieren

    # die generierte antwort dekodieren
    answer = tokenizer.decode(output[0], skip_special_tokens=True).split("Antwort: ")[1].strip()

    print(answer)

    return answer