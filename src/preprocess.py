import os
import json
from pathlib import Path

def clean_text(text):
    # Basic cleaning of clinical notes
    return text.strip().replace('\n', ' ')

def load_notes(input_dir):
    notes = []
    for file in Path(input_dir).glob('*.txt'):
        with open(file, 'r') as f:
            notes.append({"filename": file.name, "text": clean_text(f.read())})
    return notes

def save_for_model(notes, output_path):
    with open(output_path, 'w') as f:
        json.dump(notes, f, indent=2)

if __name__ == "__main__":
    notes = load_notes("../data/raw_notes")
    save_for_model(notes, "../data/processed/notes_cleaned.json")
