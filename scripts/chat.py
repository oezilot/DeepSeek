import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# Lade das Modell und den Tokenizer
model_name = "../deepseek-llm-7b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)

# Das Modell in den Evaluierungsmodus versetzen (deaktiviert Dropout usw.)
model.eval()

# Funktion, um Eingaben zu verarbeiten und eine Antwort zu generieren
def generate_response(prompt):
    # Tokenisiere die Eingabe
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generiere eine Antwort
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
    
    # Dekodiere die Ausgabe und gib sie zurück
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Interaktive Eingabe
while True:
    user_input = input("Du: ")
    if user_input.lower() == 'exit':
        print("Skript beendet.")
        break
    
    response = generate_response(user_input)
    print(f"Modell: {response}")
