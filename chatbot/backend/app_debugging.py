from flask import Flask, request, send_from_directory


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


 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True) # wenn man app.run startet startet der service der auf die hier vordefinierten paths lausht. wann auch immer ein requst gemacht wird wird die dort definerte funktion aufgerufen und der return wert als response zurückgegeben!