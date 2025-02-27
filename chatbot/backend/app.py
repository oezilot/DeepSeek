import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chatbot/backend")
from run_model import generate_response_to_input, load_model_essentials

from flask import Flask, request, send_from_directory


app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chatbot/frontend")

load_model_essentials() # die globalen variablen werden initialisiert und das model geladen!

# das wird aufgerufen sobald man / reqestet
@app.route("/")
def serve_html():
    return send_from_directory(app.static_folder, "app.html") # bei flask muss es immer ein return haben


# diese funktion wird nur aufgeruefen wenn eine post-methode auf /submit ausgeführt wurde!
@app.route("/submit", methods=['POST'])
def receive_user_input():

    # der userinput bekommt über das html/javascript über eine post-request
    user_data = request.get_json()
    user_data_string = user_data['message']
    print(f"Der User Fragt: {user_data_string}")

    # die response wird von einem internen python skript generiert und an javascript/html geschickt
    response = generate_response_to_input(user_data_string)
    print(f"Der Bot antwortet: {response}")

    return response  # Optional, um eine Antwort zurückzugeben




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True) # wenn man app.run startet startet der service der auf die hier vordefinierten paths lausht. wann auch immer ein requst gemacht wird wird die dort definerte funktion aufgerufen und der return wert als response zurückgegeben!
