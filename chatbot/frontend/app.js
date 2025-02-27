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
        body: JSON.stringify({ message: promt_string })  // json-onjekt wir din json-string umgewandelt (python versteht strings ud javascript versteht jsons)
    })
}
// diese funktion wartet aus eine antwort des backends, das warten startet sobal  das frontend einen request versendet hat
async function receive_response_from_backend() {
    try {
        let response = await fetch("http://127.0.0.1:5001/response"); // Warten auf Antwort
        let data = await response.json(); // JSON verarbeiten
        console.log("🤖 Bot-Antwort:", data); // Die Antwort ausgeben

        // Antwort in das HTML einfügen
        document.getElementById("bot").innerHTML += "<br>" + data + "<br>";
    } catch (error) {
        console.error("❌ Fehler beim Abrufen der Antwort:", error);
    }
}

// diese funktion stellt den input des users sofort dar auf dem html dar (onclick-event)
function chat() {
    input_value = document.getElementById("user").innerHTML += "<br>" + user_input.value + "<br>";
    send_promt_to_backend(user_input.value)
    receive_response_from_backend()
}
submit_button.addEventListener("click", chat)