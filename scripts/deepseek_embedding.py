from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# Lokales Modellverzeichnis setzen
model_path = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat"  

# Tokenizer und Modell laden
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")

# mit diesem skript will ich mithilfe des deepseek-models aus einem string einen vektor machen!
input_string = "i"

# funktion um aus einem string einen vektor zu generieren mithilfe des models
def string_to_vector(string):
    # string tekenisieren:
    string_tokenized = tokenizer(string, return_tensors="pt", padding=True, truncation=True).to(model.device)
    print(f"string_tokenized: {string_tokenized}")

    with torch.no_grad():
        vectors = model(**string_tokenized, output_hidden_states=True)
    print(f"Vektoren von allen states: {vectors}")
    
    last_hidden_state = vectors.hidden_states[-1]
    print(f"Vektor von dem last_hidden_state: {last_hidden_state}")
string_to_vector(input_string)

