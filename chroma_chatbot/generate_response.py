import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chroma")
from deepseek_embedding import string_to_tensor


import chromadb
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 📌 Modell & Tokenizer laden
MODEL_PATH = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH, torch_dtype=torch.bfloat16, device_map="auto"
)

# 📌 Verbindung zur ChromaDB-Datenbank
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten")


def deepseek_answer(query_text, n_results=1):
    """
    Nutzt ChromaDB, um den relevantesten Eintrag für die Anfrage zu finden,
    und gibt dann eine schön formulierte Antwort mithilfe von DeepSeek aus.

    Args:
        query_text (str): Die Eingabe-Frage.
        n_results (int): Anzahl der zurückzugebenden Ergebnisse aus ChromaDB.

    Returns:
        str: Eine schön formulierte Antwort von DeepSeek.
    """

    query_vector = string_to_tensor(query_text).mean(dim=1).squeeze().tolist()

    # 🔹 ChromaDB nach der semantisch ähnlichsten Geschichte durchsuchen
    query_results = collection.query(
        query_embeddings=[query_vector],  
        n_results=n_results  # Anzahl der relevantesten Ergebnisse
    )

    # 🔹 Falls keine Ergebnisse gefunden wurden
    if not query_results["documents"]:
        return "Ich konnte leider keine relevante Information finden."

    # 🔹 Relevante Informationen aus ChromaDB abrufen
    metadata = query_results["metadatas"][0][0]  # Die zugehörigen Metadaten
    title = metadata.get("title", "Unbekannte Geschichte")  # Titel abrufen
    text = metadata.get("content", "Unbekannte Geschichte")

    # 🔹 Nachrichten-Format für den DeepSeek-Prompt
    messages = [
        {"role": "system", "content": "Du bist ein hilfreicher KI-Assistent, der Fragen anhand von Hintergrundwissen beantwortet."},
        {"role": "user", "content": f"Hier ist eine relevante Geschichte:\n\nTitel: {title}\n\nInhalt: {text}\n\nNutze diese Information, um die folgende Frage möglichst schön und ausführlich zu beantworten."},
        {"role": "user", "content": f"Frage: {query_text}"},
    ]

    # 🔹 Tokenisierung im Chat-Format
    input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt").to(model.device)
    
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