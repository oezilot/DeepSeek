## Hello <3

### Instalation
1. venv einrichten und aktivieren
1. venv mit den requirements: pip install requirements
2. model herunterladen: git clone https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat models/deepseek-r1-7b
3. alle ordner und files vorbereiten: knowledgebases ordner und datasets-ordner muss befüllt werden

### alle Quellen
- https://github.com/chroma-core/chroma 
- js und html: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input

### errors bei der installation
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

## alle files erklärt und theorie
- der code selber erkläre ich in jedem skript in den commentaren
- jeder ordner hat ein readme.md in dem ein wenig theorie steht, fragen und erkenntnisse

## My Scripts and how to run them and what they do
In this repo you will find a couple of different scripts! I will explain their content and how to run them:

dependency scripts:
alle davon sind im scripts-ordner

main scripts:
diese scripts sind in diversen unterordnern
- fill database
- query database
- chat with your data through frontend
- chat with deepseek through terminal
- chat with deepseek through frontend
- javascript loader for the frontends