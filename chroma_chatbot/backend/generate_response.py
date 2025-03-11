'''
Dieses skript generiert zu einem promt eine antwort. 
es kann nur auf dige antworten die etwas mit den informationen in der chromadb haben antworten

folgendes macht das model:
- model initialisieren
- verbindung zur datenbank
- match von promt und datenbankeintrag finden
- deepseek generiert eine antwor mit den metadaten und dem promt
'''

import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chroma")
from deepseek_embedding import string_to_tensor

import chromadb
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 📌 pretrained Modell & Tokenizer laden
MODEL_PATH = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat" # hier befindet sich das model (weights, biases, dimensionen, alphabet, andere konfigs)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH) # den tokenizer konfigurieren basierend des alphabets des modells (je nach model werden strings anders tokenisiert)
model = AutoModelForCausalLM.from_pretrained( # das model wird geladen (es wird ein Pytorch-modell erstellt mit den informationen aus dem config.js und den weights/biases)
    MODEL_PATH, torch_dtype=torch.bfloat16, device_map="auto"
)

# 📌 Verbindung zur ChromaDB-Datenbank herstellen die bereits gefüllt ist mit den embeddings
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten")

def deepseek_answer(query_text, n_results=1):

    query_vector = string_to_tensor(query_text).mean(dim=1).squeeze().tolist() # mit deepseek aus einem string einen semantischen vektor generieren

    query_results = collection.query( # chromadb nach dem semantisch ähnlichsten vektor durchsuchen
        query_embeddings=[query_vector],  
        n_results=n_results  # Anzahl der relevantesten Ergebnisse (in diesem fall nur eine geschihte und zwar die ähnlichte zurück geben)
    )

    # 🔹 Falls keine Ergebnisse gefunden wurden
    if not query_results["documents"]:
        return "Ich konnte leider keine relevante Information finden."

    # 🔹 Relevante Informationen aus ChromaDB abrufen (aus der sqlite datenbank)
    metadata = query_results["metadatas"][0][0]  # Die zugehörigen Metadaten
    title = metadata.get("title", "Unbekannte Geschichte")  # Titel abrufen
    text = metadata.get("content", "Unbekannte Geschichte") # den text abrufen

    # 🔹 Nachrichten-Format für den DeepSeek-Prompt
    messages = [
        {"role": "system", "content": "Du bist ein hilfreicher KI-Assistent, der Fragen anhand von Hintergrundwissen beantwortet."},
        {"role": "user", "content": f"Hier ist eine relevante Geschichte:\n\nTitel: {title}\n\nInhalt: {text}\n\nNutze diese Information, um die folgende Frage möglichst schön und ausführlich zu beantworten."},
        {"role": "user", "content": f"Frage: {query_text}"},
    ]

    input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt").to(model.device) # den promt für deepseek in tokenform bringen
    
    # 🔹 DeepSeek generiert eine Antwort
    with torch.no_grad():
        output = model.generate(input_ids, max_new_tokens=200)  # Antwort generieren

    # 🔹 Antwort dekodieren und ausgeben
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer

# 📌 Beispielaufruf der Funktion
frage = "Wie heißt der Rock Frosch?"
antwort = deepseek_answer(frage)
print("🤖 DeepSeek Antwort:", antwort)