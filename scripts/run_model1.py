import torch
# 3 module der hugging face transformers bibliotheke
'''
erklärung dieser funktionen:
- AutoTokenizer -> wandelt text in zahlen (tokens) um
- AutoModelForCausalLM -> lädt das model das wir heruntergeladen haben (es muss vortrainiert sein und weights haben?)
- GenerationConfig -> lädt das config mit den parametern fr das ausführen
'''
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# Modellpfad (unter diesem pfad befindet sich das geklonte repo mit alen jsons und den weights)
model_path = "/home/zoe/Projects/DeepSeek/deepseek-llm-7b-chat"  

############# PROZESSOR (CUDA VS. CPU) #######################

# wenn folgender wert true ist ist gpu verfügbar um das model dort zu laden und wenn nicht muss man es über den cpu machen!
print(f"Cuda availability: {torch.cuda.is_available()}")


############# TOKENIZER #######################

# Tokenizer laden, diese funktion sucht im aktuellen verzeichnis nach den dateien tokenizer.json und tokenizer_config.json und lädt diese
# der tokenizer baut den string nach mit einer kombination des vokabulars! die indizes dieser vocis die gebraucht werden um den string zu bauen sind dann eine teil der tokensliste
# die attention_mask gibt an wie lange der string ist. wenn man als ausgabe zum beispiel einen token will der 10 zeichen hat aber dein string nur 3 zeichen braucht dann sind 7 zeichen der liste eine 0 damit diese ignoriert werden weil sie irrelevant sind! wenn man aber keien länge forsiert ist immer 1 in dieser liste
tokenizer = AutoTokenizer.from_pretrained(model_path)
string = "zoi! pusi ist cool"
token = tokenizer(string)
# tokenizer testen (input: string, output: liste mit ids (input_ids und liste mit 1 (attention_mask))))
print(f"den String '{string}' in einen token verwandeln: {token}")


############# MODEL #######################

# Modell laden (falls keine gpu vorhanden wird das mit dem cpu automatish)
# mit dem config wird ein leeres neuronales netz gebaut und mit den gewichten wird dieses dann gefüllt
model = AutoModelForCausalLM.from_pretrained(
    model_path, # in desem ordner sind die .bin files mit den weights
    torch_dtype=torch.bfloat16,  # Nutzt bfloat16 für Effizienz (wenn GPU verfügbar)
    device_map="auto"            # Lädt Modell automatisch auf GPU, falls vorhanden
)
# überpfürfen auf was das model geladen wurde (gpu oder cpu)
print(f"das model wird auf {model.device} geladen")
# ein paar vektoren der weights ansehen
# print(f"das sind vektoren für die weights: {name, param.shape for name, param in model.named_parameters()}")


############# JSONS #######################

# generation_config.json
generation_config = GenerationConfig.from_pretrained(model_path)
# falls das moel keine paddingtokens generiert werden die endof sequence tokens dafür genutzt
if generation_config.pad_token_id is None:
    generation_config.pad_token_id = generation_config.eos_token_id
# Nutzereingabe für Chat, damit das model weiss wer er ist kann man es bereits vorbereiten mit dieser message. dann weiss es wie weiter antworten
messages = [
    {"role": "user", "content": "Who are you?"}
]

# den userinput vektorisieren
input_tensor = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", padding=True)
#print(f"Das ist das Cat-Template: {tokenizer.chat_template}")
#print(f"das sind alle möglichkeiten für tokenizer-infod zu holen mit tokenizer.x: {dir(tokenizer)}")
# help(tokenizer.encode)# dokumentation für die einzelnen funktionen

# Setze attention_mask explizit
input_tensor["attention_mask"] = (input_tensor["input_ids"] != tokenizer.pad_token_id).long()

# generierung einer antwort auf userinput (müsste das nicht eine while-funktion sein? der bot muss ja immer antworten solange der chat am laufen ist!)
outputs = model.generate(input_tensor.to(model.device), max_new_tokens=100)
print(f"this ist the output of the bot but tokenized (das sind alle outputs die der bot je generiert hatte. wenn man immer nur die neuste der generierten nahcrichten will muss man outputs[0][input_tensor.shape[1]:]): {outputs[0]}")
# die antwort des bots von der vektorform in die menschenform verändern
#result = tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)
#print("🤖 DeepSeek Antwort:", result)