'''
dieses skript testet nur ob das mit der kommunikation zwischen frontend und backend funktioniert! app.py ist das richtige wo auch eine antwort des chat-botd kommt und nicht etwas erfundenen
'''

from flask import Flask, request, send_from_directory, jsonify


# variablen
app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chatbot/frontend")

chat_history = []

# homeseite
@app.route("/")
def serve_html():
    return send_from_directory(app.static_folder, "app_debugging.html") # bei flask muss es immer ein return haben


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
    bot_output = f"XX{chat_history[-1]["user_input"]}XX"
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