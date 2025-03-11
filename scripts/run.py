'''
Dieses skript initialisiert das modell und lässt es laufen

argumente:
- der pfad zum model
'''

from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# ------------- INIT MODEL ----------------
model_path = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat"  

tokenizer = AutoTokenizer.from_pretrained(model_path) # den tokenizer konfigurieren basierend des alphabets des modells (je nach model werden strings anders tokenisiert)
model = AutoModelForCausalLM.from_pretrained( # das model wird geladen (es wird ein Pytorch-modell erstellt mit den informationen aus dem config.js und den weights/biases)
    model_path, torch_dtype=torch.bfloat16, device_map="auto"
)

print("Das Model wurde initialisiert!")

'''
fragen:
- warum wenn ich dieses script irgendwo importiere kommt der balken welcher das model anzeigt beim laden 2mal?
'''