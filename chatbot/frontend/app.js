// this documents sends the frontendcode to the backend and does button-functionality and stuff

// this variable hold the sting that the user gave as a promt
var user_input = document.getElementById("user_input");
var submit_button = document.getElementById("submit");

// diese funktion sendet den userinput zu backend
function send_promt_to_backend(promt_string) {
    fetch("http://127.0.0.1:5001/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: promt_string
    })
}

function get_response_from_backend() {
    fetch()
}

// diese funktion zeigt deine anfreage an den bot im chatverlauf an:
function user() {
    // display the user_input in the chat-box
    input_value = document.getElementById("user").innerHTML += "<br>" + user_input.value + "<br>";
    // sende den gesammelten input des users an das python backend
    //send_promt_to_backend(user_input.value.trim());
}
submit_button.addEventListener("click", user)