import sys
sys.path.append("/home/zoe/Projects/DeepSeek/scripts")

from flask import Flask, request, send_from_directory, jsonify # libraries für die flask app
import chromadb

import run # das model importieren
from generate import generate_response, find_chroma_match # funktionen um eine deepseek antwort zu generieren
from embedding import string_to_tensor


# variablen
app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chroma_chatbot/frontend")
chat_history = []


# das model laufen lassen (das passiert bim importen)


# Verbindung zur bestehenden ChromaDB-Datenbank
client = chromadb.PersistentClient(path="/home/zoe/Projects/DeepSeek/knowledgebases")
collection = client.get_or_create_collection("Geschichten") # wenn man die cellection gettet oder kreiert muss man immer de embeddingfunktione angeben! -> client.get_collection(name="my_collection", embedding_function=emb_fn)


# das wird aufgerufen sobald man / reqestet
@app.route("/")
def serve_html():
    return send_from_directory(app.static_folder, "app.html") # bei flask muss es immer ein return haben

# nachricht erhalten
@app.route("/submit", methods=['POST'])
def receive_user_input():

    global chat_history

    # der userinput kommt über das html/javascript über eine post-request
    user_data = request.get_json()
    user_data_string = user_data['message']
    # den neusten inputwert dem chatverlauf hinzufügen, output vorerst mal none setzen
    chat_history.append({"user_input":user_data_string, "bot_output":None})
    # der letzte input-wert printen
    print(f"Der User Fragt: {chat_history[-1]["user_input"]}")
    # die gesamte histoy printen
    print(f"Chat-History: {chat_history}")

    # das return geht dann zum browser wo javascript es abholen kann
    return chat_history


# nachricht versenden
@app.route("/response", methods=['GET'])
def send_bot_output():

    global chat_history

    # den userpromt in einen vektor umwandeln
    query_vector = string_to_tensor(chat_history[-1]["user_input"], run.model, run.tokenizer).mean(dim=1).squeeze().tolist()
    # die antwort von depseek auf deine anfrage (generate.py)
    bot_output = generate_response(chat_history[-1]["user_input"], run.model, run.tokenizer, find_chroma_match(query_vector, collection))    
    # bot-rsponse der history hinzufügen
    chat_history[-1]["bot_output"] = bot_output

    # der letzte output-wert printen
    print(f"Der Bot antwortet: {chat_history[-1]["bot_output"]}")
    # die gesamte histoy printen
    print(f"Chat-History: {chat_history}")

    # das return geht dann zum browser wo javascript es abholen kann
    return jsonify(chat_history[-1]["bot_output"]) # den string in ein json-onjekt verwandeln damit es javaskript versteht


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True) # wenn man app.run startet startet der service der auf die hier vordefinierten paths lausht. wann auch immer ein requst gemacht wird wird die dort definerte funktion aufgerufen und der return wert als response zurückgegeben!