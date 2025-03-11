'''
dieses skript generiert eine deepseek-embedding für einen string

link zu embedding funktiond mit chroma: https://docs.trychroma.com/docs/embeddings/embedding-functions 
'''

from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

# ---------------------------------------

# funktion um aus einem string einen vektor zu generieren mithilfe des models
def string_to_tensor(string, model, tokenizer):

    # string tekenisieren:
    string_tokenized = tokenizer(string, return_tensors="pt", padding=True, truncation=True).to(model.device)
    #print(f"string_tokenized: {string_tokenized}")

    # den tokenisierten string durch das model durchlassen und eine liste von tensoren zurückgeben wo jeder tensor eine schicht des modell repräsentiert
    with torch.no_grad():
        vectors = model(**string_tokenized, output_hidden_states=True) # modell-objekt mit folgendem drin, ein dictionary mit: (logits(token-wk für vorhersage), hidden_states(liste mit tensoren für die hiddenstates des modells), past_key_values)
        hidden_states = vectors["hidden_states"] # liste von layers wo jedes layer für jeden token einen vektor besitzt! (1 tensor = mulidimensionaler vektor!)
        last_tensor = hidden_states[-1]

    # anzahl schichten und den inhalt des schichtentensors
    #print(f"Anzahl Schichten: {len(hidden_states)}, Tensoren von allen states: {hidden_states}")

    # der letzte schichtentensor (enthält für jedes token einen vektor)
    #print(f"Tensor von dem last_hidden_state: {hidden_states[-1]}, Die shape des tensors: {hidden_states[-1].shape}") 

    #print(f"Shape: {hidden_states[-1].shape}")

    # der zusammengefasste vektor wäre:
    #print(f"Zusammengefasster Vektor für chromaDB: {last_tensor.mean(dim=1).squeeze().tolist()}") # diese funktionen können nur angewendet werden wenn man es auf einen tensor-typ anwendet

    return last_tensor

'''
#string_to_tensor(input_string, model, tokenizer)
tensor = torch.randn(2, 3, 2)
print(tensor) # .mean = nimmt das mittel. anzahl dimeasionen - dim = wie viele dimensionen sollte der outputvektor haben (dimension = 2X3X2)
print(tensor.mean()) # gibt eine einzige zahl heraus
print(tensor.mean(dim=1)) # gibt einen tensr in der grösse des urpsurchstensors heraus (dim-3 -> 3X2, dim-2 -> 2X2, dim-1 -> 2X2, dim0 -> 2X3X2, dim1 -> 2X2, dim2 -> dimeansion = 2X3)... expectied dim range = [-3, 2]
print(tensor.mean(dim=1).squeeze().tolist())
'''

# ---------------------------------------

# einen tensor zusammenfassen sodass er eindimensionale ist (mean) und dass die batchgrösse entfernt wird
#tensor_mean = string_to_tensor(input_string).mean(dim=1).squeeze()