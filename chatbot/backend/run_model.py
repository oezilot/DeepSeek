from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# Lokales Modellverzeichnis setzen
model_path = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat"  

# Tokenizer und Modell laden
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")

# Generierungskonfiguration laden
generation_config = GenerationConfig.from_pretrained(model_path)

# Falls das Modell kein explizites Padding-Token hat, setzen wir es auf EOS
if generation_config.pad_token_id is None:
    generation_config.pad_token_id = generation_config.eos_token_id

def generate_response_to_input(input_string):
    # Beispiel-Chatverlauf
    messages = [
        {"role": "system", "content": "You are a helpful assistant who answers briefly."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": input_string}
    ]

    # Eingabe tokenisieren und Padding aktivieren
    input_ids = tokenizer.apply_chat_template(
        messages, 
        add_generation_prompt=True, 
        return_tensors="pt", 
        padding=True
    )

    # attention_mask manuell erstellen
    attention_mask = (input_ids != tokenizer.pad_token_id).long()

    # Modell generiert die Antwort
    outputs = model.generate(
        input_ids.to(model.device), 
        attention_mask=attention_mask.to(model.device), 
        max_new_tokens=100
    )

    # Antwort dekodieren
    result = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)

    return result
print(generate_response_to_input("Tell me something about germany"))