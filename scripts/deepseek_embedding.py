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

    # den tokenisierten string durch das model durchlassen und eine liste von tensoren zurückgeben wo jeder tensor eine schicht des modell repräsentiert
    with torch.no_grad():
        vectors = model(**string_tokenized, output_hidden_states=True) # modell-objekt mit folgendem drin, ein dictionary mit: (logits(token-wk für vorhersage), hidden_states(liste mit tensoren für die hiddenstates des modells), past_key_values)
        hidden_states = vectors["hidden_states"] # liste von layers wo jedes layer für jeden token einen vektor besitzt! (1 tensor = mulidimensionaler vektor!)

    # anzahl schichten und den inhalt des schichtentensors
    print(f"Anzahl Schichten: {len(hidden_states)}, Tensoren von allen states: {hidden_states}")
    
    # der letzte schichtentensor (enthält für jedes token einen vektor)
    print(f"Tensor von dem last_hidden_state: {hidden_states[-1]}") 


string_to_vector(input_string)

