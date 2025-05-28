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

