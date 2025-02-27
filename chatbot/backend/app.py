import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chatbot/backend")
from run_model import generate_response_to_input, load_model_essentials

from flask import Flask, request, send_from_directory


app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chatbot/frontend")

load_model_essentials() # die globalen variablen werden initialisiert und das model geladen!

# globale varable (liste mit dictionares mit dem userinput und dem botoutput)
chat_history = []

# das wird aufgerufen sobald man / reqestet
@app.route("/")
def serve_html():
    return send_from_directory(app.static_folder, "app.html") # bei flask muss es immer ein return haben


# diese funktion wird nur aufgeruefen wenn eine post-methode auf /submit ausgeführt wurde!
@app.route("/submit", methods=['POST'])
def receive_user_input():

    global chat_history

    # der userinput bekommt über das html/javascript über eine post-request
    user_data = request.get_json()
    user_data_string = user_data['message']
    chat_history.append({"user_input" : user_data_string, "bot_output" : None})
    print(chat_history)
    print(f"Der User Fragt: {user_data_string}")

    # das return geht dann zum browser wo javascript es abholen kann
    return ""
    

@app.route("/response", methods=['GET'])
def generate_response():

    global chat_history
    last_index = len(chat_history)-1

    # die response wird von einem internen python skript generiert und an javascript/html geschickt
    response = generate_response_to_input(chat_history[-1]["user_input"])
    # die response des bots dem chatverlauf hinzufügen
    chat_history[-1]["bot_output"] = response
    print(f"Der Bot antwortet: {response}")

    return jsonify({"response": response})




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True) # wenn man app.run startet startet der service der auf die hier vordefinierten paths lausht. wann auch immer ein requst gemacht wird wird die dort definerte funktion aufgerufen und der return wert als response zurückgegeben!


# erkenntnisse: 
# - die methode jeder route bezieht sich nicht darauf was python tut sondern was das frontend tun will mit dieser route. python füllt quasi diesen briefkasten mit dem returnstatement der funktion unter der route definiert und das fronent macht einen request auf den inhalt dieses briefkastens (PUT, GET, DELETE, etc)
# - die /parameter eines URI sind dafür da als quasi adressen wohin http-requests hingeschickt werden und wo die responses zu holen sind! (können mehrere verschiedene requests an der gleichen adresse sein?)

# fragen:
# - gibt es einen gemeinsamen route für request und response oder sind das seperate?
# - wenn ein request geholt wird ist dann der briefkasten leer?