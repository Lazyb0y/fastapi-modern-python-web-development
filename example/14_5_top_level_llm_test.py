from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig

app = FastAPI()

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
config = GenerationConfig(max_new_tokens=200)


@app.get("/ai")
def prompt(line: str) -> str:
    tokens = tokenizer(line, return_tensors="pt")
    outputs = model.generate(**tokens, generation_config=config)
    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return result[0]
