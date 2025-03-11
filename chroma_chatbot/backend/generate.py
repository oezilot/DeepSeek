'''
dieses skript generiert eine antwort zu einem promt. die argumente sind das model und der tokenizer und eine chomadatenbank die gefüllt ist
'''

import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chroma")
from deepseek_embedding import string_to_tensor

import chromadb
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


MODEL_PATH = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat" # hier befindet sich das model (weights, biases, dimensionen, alphabet, andere konfigs)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH) # den tokenizer konfigurieren basierend des alphabets des modells (je nach model werden strings anders tokenisiert)
model = AutoModelForCausalLM.from_pretrained( # das model wird geladen (es wird ein Pytorch-modell erstellt mit den informationen aus dem config.js und den weights/biases)
    MODEL_PATH, torch_dtype=torch.bfloat16, device_map="auto"
)

# diese funktion sucht nach dem datenpunkt mit den meisten ähnlichkeiten
def find_query_match(query_text, model, n_results):

    # promt in einen vektor verwandeln
    query_vector = string_to_tensor(query_text, model, tokenizer).mean(dim=1).squeeze().tolist()

    # einen match in der datenbank suchen (kürzeste distanz) -> es gibt die zeile der tabelle mit den metadaten zurück die am ähnlichsten ist zum promt
    query_match = collection.query(query_embeddings=[query_vector], n_results=n_results)

    # falls es keinen match gibt
    if not query_match["documents"]:
        return "Ich konnte leider keine relevante Information finden."

    return query_match


# diese funktion generiert mit einem model und einem tokenizer eine antwort
def generate_response(query_text, model, tokenizer, n_results=1):   

    data = find_query_match(query_text, model, n_results)

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
antwort = generate_response(frage, model, tokenizer)
print("🤖 DeepSeek Antwort:", antwort)