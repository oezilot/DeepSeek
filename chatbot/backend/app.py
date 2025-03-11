'''
dieses script macht lädt das model, generiert eine antwort und kommuniziert mit dem js.code des frontends
'''
import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chatbot/backend")
from run_model import generate_response_to_input, load_model_essentials # funktionen impotrieren: eine antwort generieren, das model welches die antwort generiert

from flask import Flask, request, send_from_directory, jsonify # python libraries


app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chatbot/frontend")

load_model_essentials() # die globalen variablen werden initialisiert und das model geladen!

# globale varable (liste mit dictionares mit dem userinput und dem botoutput)
chat_history = []

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

    # die antwort wird so konstruiert dass sie immer 2 XX vor und hinter den user-input macht
    bot_output = generate_response_to_input(chat_history[-1]["user_input"])
    # bot-rsponse der history hinzufügen
    chat_history[-1]["bot_output"] = bot_output

    # der letzte output-wert printen
    print(f"Der Bot antwortet: {chat_history[-1]["bot_output"]}")
    # die gesamte histoy printen
    print(f"Chat-History: {chat_history}")

    # das return geht dann zum browser wo javascript es abholen kann
    return jsonify(chat_history[-1]["bot_output"]) # den string in ein json-onjekt verwandeln damit es javaskript versteht


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True) # wenn man app.run startet startet der service der auf die hier vordefinierten paths lausht. wann auch immer ein requst gemacht wird wird die dort definerte funktion aufgerufen und der return wert als response zurückgegeben!


# erkenntnisse: 
# - die methode jeder route bezieht sich nicht darauf was python tut sondern was das frontend tun will mit dieser route. python füllt quasi diesen briefkasten mit dem returnstatement der funktion unter der route definiert und das fronent macht einen request auf den inhalt dieses briefkastens (PUT, GET, DELETE, etc)
# - die /parameter eines URI sind dafür da als quasi adressen wohin http-requests hingeschickt werden und wo die responses zu holen sind! (können mehrere verschiedene requests an der gleichen adresse sein?)

# fragen:
# - gibt es einen gemeinsamen route für request und response oder sind das seperate?
# - wenn ein request geholt wird ist dann der briefkasten leer?