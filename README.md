# OMOP LLM Extraction Pipeline

This repository contains a modular pipeline to extract structured data from unstructured clinical notes using large language models (LLMs) and map it into the OMOP Common Data Model (CDM).

## Project Structure
```
├── data/                # Input and annotation files
├── models/              # Finetuned models or weights
├── omop/                # Schema files or example SQL
├── outputs/             # Model output JSONs
├── prompts/             # Prompt templates and few-shot examples
├── src/                 # Core source code
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Setup
1. Clone the repo:
```bash
git clone https://github.com/j-klawson/omop-llm-extraction 
cd omop-llm-extraction
```

2. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Generate a Synthea Test Set 

```
./scripts/setup_synthia.sh
python src/generate_synthia_test_set.py
```

4. Preprocess clinical notes:
```bash
python src/preprocess.py
```

5. Run the model on preprocessed notes:
```bash
python src/run_model.py
```

6. Evaluate the model (optional):
```bash
python src/evaluate.py
```

7. Load extracted data into OMOP:
```bash
python src/load_to_omop.py
```

## Data Format

### Input (raw notes)
Plain `.txt` files under `data/raw_notes/`

### Output (model_outputs.json)
```json
[
  {
    "filename": "note1.txt",
    "output": {
      "condition_occurrence": [...],
      "observation": [...],
      "drug_exposure": [...],
      "person": [...]
    }
  }
]
```

## Notes
- Ensure your OMOP database is up and running before calling `load_to_omop.py`
- Replace placeholders in SQL logic with real insert templates

## License

This project is licensed under the GNU General Public License version 2 (GPLv2).  
See the [COPYING](./COPYING) file for details.


---