import json

def run_model_on_note(note, model=None):
    # Placeholder for LLM inference
    return {
        "condition_occurrence": [],
        "observation": [],
        "drug_exposure": [],
        "person": []
    }

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

