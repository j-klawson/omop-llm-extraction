import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_ID = "mistralai/Mistral-7B-Instruct"

print("Loading model... This may take a few minutes the first time.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.float16
)
llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

def create_prompt(note):
    return f"""
You are a clinical data extractor. Convert the following note into OMOP CDM:
"{note}"

Output as JSON with keys: condition_occurrence, observation, drug_exposure, person.
"""

def run_model_on_note(note_text):
    prompt = create_prompt(note_text)
    response = llm_pipeline(prompt, max_new_tokens=512, temperature=0.1)
    try:
        # Optional: parse the JSON from generated text
        generated = response[0]["generated_text"].split("Output:")[-1].strip()
        return json.loads(generated)
    except Exception as e:
        print("Error parsing model output:", e)
        return {}

def process_notes(input_path, output_path):
    with open(input_path, 'r') as infile:
        notes = json.load(infile)
    results = []
    for note in notes:
        output = run_model_on_note(note['text'])
        results.append({"filename": note["filename"], "output": output})
    with open(output_path, 'w') as outfile:
        json.dump(results, outfile, indent=2)

if __name__ == "__main__":
    process_notes("../data/processed/notes_cleaned.json", "../outputs/model_outputs.json")