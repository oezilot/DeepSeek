from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# Modellpfad definieren
model_path = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat"

# Globale Variablen für das Modell und den Tokenizer
tokenizer = None
model = None
generation_config = None

# Modell nur einmal laden
def load_model_essentials():
    global tokenizer, model, generation_config

    if tokenizer is None or model is None:  # Verhindert doppeltes Laden
        print("🚀 Lade Modell...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16, device_map="auto")
        generation_config = GenerationConfig.from_pretrained(model_path)

        # Falls das Modell kein explizites Padding-Token hat, setzen wir es auf EOS
        if generation_config.pad_token_id is None:
            generation_config.pad_token_id = generation_config.eos_token_id

        print("✅ Modell erfolgreich geladen!")
#load_model_essentials()

# Antwort generieren, ohne das Modell neu zu laden
def generate_response_to_input(input_string):
    global tokenizer, model  # Globale Variablen nutzen

    if tokenizer is None or model is None:
        raise ValueError("⚠️ Fehler: Modell wurde nicht geladen! Bitte load_model_essentials() vorher aufrufen.")

    # Beispiel-Chatverlauf
    messages = [
        {"role": "system", "content": "You are a helpful assistant who answers briefly."},
        {"role": "user", "content": input_string}
    ]

    # Eingabe tokenisieren
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        padding=True
    )

    attention_mask = (input_ids != tokenizer.pad_token_id).long()

    # Modell generiert die Antwort
    outputs = model.generate(
        input_ids.to(model.device),
        attention_mask=attention_mask.to(model.device),
        max_new_tokens=100
    )

    result = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
    return result

#generate_response_to_input("Tell me something about Switzerland")
#generate_response_to_input("Tell me something about germany")