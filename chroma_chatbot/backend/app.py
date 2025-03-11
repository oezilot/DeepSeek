'''
dieses script macht lädt das model, generiert eine antwort und kommuniziert mit dem js.code des frontends
'''
import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chroma_chatbot/backend")
from generate import generate_response

from flask import Flask, request, send_from_directory, jsonify # python libraries


# ---------------------------------

# das model initialisieren
MODEL_PATH = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat" # hier befindet sich das model (weights, biases, dimensionen, alphabet, andere konfigs)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH) # den tokenizer konfigurieren basierend des alphabets des modells (je nach model werden strings anders tokenisiert)
model = AutoModelForCausalLM.from_pretrained( # das model wird geladen (es wird ein Pytorch-modell erstellt mit den informationen aus dem config.js und den weights/biases)
    MODEL_PATH, torch_dtype=torch.bfloat16, device_map="auto"
)

# verbindung zur datenbank herstellen
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases") # datenbank-verbindung
collection = client.get_or_create_collection("Geschichten") # metadaten laden

# die app initialisieren
app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chroma_chatbot/frontend")

# ---------------------------------

# eine antwort mit der generate-funktion generieren



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True) # wenn man app.run startet startet der service der auf die hier vordefinierten paths lausht. wann auch immer ein requst gemacht wird wird die dort definerte funktion aufgerufen und der return wert als response zurückgegeben!