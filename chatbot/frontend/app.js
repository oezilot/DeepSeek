// this documents sends the frontendcode to the backend and does button-functionality and stuff

// ----------------- VARIABLES ----------------

// this variable holds the string that the user gave as a promt
var user_input = document.getElementById("user_input");

// this variable represents the send-message-button
var submit_button = document.getElementById("submit");


// ----------------- FUNKTIONS ----------------

// diese funktion sendet den userinput zum backend
function send_promt_to_backend(promt_string) {
    fetch("http://127.0.0.1:5001/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: promt_string
    })
}

// diese funktion stellt den input des users sofort dar auf dem html dar (onclick-event)
function display_user_input() {
    input_value = document.getElementById("user").innerHTML += "<br>" + user_input.value + "<br>";
}
submit_button.addEventListener("click", display_user_input)

// diese funktion wartet auf eine antwort und holt die antwort des bots vom backend sobald diese eingetroffen ist
async function get_response_from_backend() {
    let response = await fetch("http://127.0.0.1:5001/response");
    let response_data = await response.json();
    console.log(response);
    return response_data;
}

// diese funktion stellt die erhaltene information des backends dar sobald diese eingetroffen ist
var bot_history = document.getElementById("bot").innerHTML += "<br>" + get_response_from_backend() + "<br>";