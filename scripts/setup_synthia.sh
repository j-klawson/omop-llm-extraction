# scripts/setup_synthea.sh
#!/bin/bash

# This script installs and runs Synthea to generate synthetic health records

set -e

# Set output directory
OUTPUT_DIR="synthea/output"
mkdir -p $OUTPUT_DIR

# Clone Synthea if it doesn't exist
if [ ! -d "synthea" ]; then
  git clone https://github.com/synthetichealth/synthea.git
  cd synthea
else
  cd synthea
  git pull
fi

# Run Synthea with default settings for Massachusetts
./gradlew build
./run_synthea -p 100 -cs 0 -o $OUTPUT_DIR Massachusetts

cd ..
echo "✅ Synthea data generated in $OUTPUT_DIR"

# src/generate_synthea_testset.py
import os
import json
import random
import pandas as pd
from pathlib import Path

RAW_NOTES_DIR = "../data/raw_notes"
ANNOTATIONS_DIR = "../data/annotations"
SYN_DATA_DIR = "../synthea/output/csv"

CONDITIONS_FILE = os.path.join(SYN_DATA_DIR, "conditions.csv")
MEDICATIONS_FILE = os.path.join(SYN_DATA_DIR, "medications.csv")
PATIENTS_FILE = os.path.join(SYN_DATA_DIR, "patients.csv")

TEMPLATE = """Patient is a {age} year old {gender} diagnosed with {condition}.
They have been prescribed {medication} for treatment."""


def load_tables():
    conditions = pd.read_csv(CONDITIONS_FILE)
    meds = pd.read_csv(MEDICATIONS_FILE)
    patients = pd.read_csv(PATIENTS_FILE)
    return conditions, meds, patients


def generate_synthetic_note(pid, conditions, meds, patients):
    row = patients[patients["Id"] == pid].iloc[0]
    gender = row["Gender"]
    birth_year = int(row["BIRTHDATE"].split("-")[0])
    age = 2025 - birth_year

    patient_conditions = conditions[conditions["PATIENT"] == pid]
    patient_meds = meds[meds["PATIENT"] == pid]

    if patient_conditions.empty or patient_meds.empty:
        return None, None

    condition = patient_conditions.iloc[0]["DESCRIPTION"]
    medication = patient_meds.iloc[0]["DESCRIPTION"]

    note = TEMPLATE.format(age=age, gender=gender, condition=condition, medication=medication)
    ground_truth = {
        "condition_occurrence": [{"condition_concept_name": condition}],
        "drug_exposure": [{"drug_name": medication}],
        "observation": [],
        "person": [{"age": age, "gender": gender}]
    }
    return note, ground_truth


def generate_notes(n=10):
    conditions, meds, patients = load_tables()
    selected_patients = patients.sample(n)

    Path(RAW_NOTES_DIR).mkdir(parents=True, exist_ok=True)
    Path(ANNOTATIONS_DIR).mkdir(parents=True, exist_ok=True)

    all_ground_truth = []
    for i, row in selected_patients.iterrows():
        pid = row["Id"]
        note, gt = generate_synthetic_note(pid, conditions, meds, patients)
        if note and gt:
            fname = f"note_{pid}.txt"
            with open(os.path.join(RAW_NOTES_DIR, fname), 'w') as f:
                f.write(note)
            all_ground_truth.append({"filename": fname, "output": gt})

    with open(os.path.join(ANNOTATIONS_DIR, "ground_truth.json"), 'w') as out_json:
        json.dump(all_ground_truth, out_json, indent=2)


if __name__ == "__main__":
    generate_notes(n=10)

