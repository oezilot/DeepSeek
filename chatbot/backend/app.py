import sys
sys.path.append("/home/zoe/Projects/DeepSeek/chatbot/backend")
from run_model import generate_response_to_input

from flask import Flask, request, send_from_directory


app = Flask(__name__, static_folder="/home/zoe/Projects/DeepSeek/chatbot/frontend")

# das wird quasi immer aufgerufen
@app.route("/")
def serve_html():
    return send_from_directory(app.static_folder, "app.html")

'''
# diese funktion wird nur aufgeruefen wenn eine post-methode auf /submit ausgeführt wurde!
@app.route("/submit", methods=['POST'])
def receive_user_input():

    user_data = request.get_json()
    user_data_string = user_data['message']
    print(user_data_string)

    response = generate_response_to_input(user_data_string)
    print(response)

    return response  # Optional, um eine Antwort zurückzugeben
'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)