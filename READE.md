## Hello <3

### Instalation
1. venv einrichten und aktivieren
1. venv mit den requirements: pip install requirements
2. model herunterladen: git clone https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat models/deepseek-r1-7b

### Das macht die ChromaDB:
1. Chroma nimmt den Text aus documents und wandelt ihn automatisch in Vektoren um.
2. Diese Vektoren werden dann für die spätere Ähnlichkeitsabfrage verwendet.
3. Du kannst sofort mit der Abfrage von Dokumenten beginnen, ohne dich um die Vektorisierung zu kümmern.

### Quellen
- https://github.com/chroma-core/chroma 
- js und html: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input

### Bedeutung der Files
- config.json = modelarchitektur wird definiert (anzahl layers etc)
- generation_congig.json = hier sind parameter die beim ausführen des run-files mitgegeben werden definiert damit man das nicht bei jedem skriptaufruf schreiben muss (diese informationen werden jedes mal gebraucht um das skript auszuführen)
- pytorch_model.bin.index.json = hier steht geschrieben in welchem file welche weights gepeicert sind
- tokenizer_config.json = hier ist das chat_template definiert
- tokenizer.json

### erklärung der files:
- im skript erkläre ich was siesom ungefährt anhandmeines bsp machen, in folgenden links indet man diedokumentatin u diesen fnktionen:
- hier noch ein sehr hifreicher chatverlauf den ich mit chatgpt hatte (das file heisst chat.md)

### Detictive
- gibt es immer den selben token heraus für ein besitmmtes wort der ist es random?


### errors
1. Traceback (most recent call last):
```
  File "/home/zoe/Projects/DeepSeek/scripts/run_model1.py", line 35, in <module>
    model = AutoModelForCausalLM.from_pretrained(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zoe/Projects/DeepSeek/venv/lib/python3.12/site-packages/transformers/models/auto/auto_factory.py", line 564, in from_pretrained
    return model_class.from_pretrained(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/zoe/Projects/DeepSeek/venv/lib/python3.12/site-packages/transformers/modeling_utils.py", line 262, in _wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/zoe/Projects/DeepSeek/venv/lib/python3.12/site-packages/transformers/modeling_utils.py", line 3611, in from_pretrained
    raise ImportError(
ImportError: Using `low_cpu_mem_usage=True` or a `device_map` requires Accelerate: `pip install 'accelerate>=0.26.0'`
```
in diesem fall einefach die library installieren, das sollte kein problem sein!!!
    ```
    pip install 'accelerate>=0.26.0'
    ```


## My Scripts:
In this repo you will find a couple of different scripts! I will explain their content and how to run them:

1. `run_model1_gpt.py`: this skripts runs the deepseek model. in the script you define a string ehich is your promt and the terminal gives you the output the chatbot would give you
2. `test_chroma.py`: filling the chromadatabase with the use of no embedding to find out how chroma works
3. `app.py`: flask applikation which uses the run_model script to make a full applikation