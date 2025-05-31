# preprocess.py
# Copyright (C) 2025 J. Keith Lawson
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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
