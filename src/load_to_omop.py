# load_to_omop.py
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

import json
import psycopg2

def insert_into_omop(parsed_output, conn):
    # Placeholder for inserting structured data into OMOP CDM
    with conn.cursor() as cursor:
        # Example: insert condition_occurrence rows
        for condition in parsed_output.get("condition_occurrence", []):
            cursor.execute(
                "INSERT INTO condition_occurrence (condition_concept_id, ...) VALUES (%s, ...)",
                (condition["concept_id"],)
            )
    conn.commit()

def load_all_outputs(output_file, db_params):
    with open(output_file, 'r') as infile:
        entries = json.load(infile)
    conn = psycopg2.connect(**db_params)
    for entry in entries:
        insert_into_omop(entry["output"], conn)
    conn.close()

if __name__ == "__main__":
    db_credentials = {
        "dbname": "omop",
        "user": "postgres",
        "password": "yourpassword",
        "host": "localhost"
    }
    load_all_outputs("../outputs/model_outputs.json", db_credentials)

