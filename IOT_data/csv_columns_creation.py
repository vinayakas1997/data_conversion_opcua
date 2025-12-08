import csv
import json

def csv_to_dict(csv_file_path, json_output_path):
    # Detect headers
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print("Detected headers:", headers)
    columns = {}

    with open(csv_file_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Strip spaces from Japanese_Name key
            key = row['Japanese_Name'].strip()

            # Strip spaces from all other fields
            value = {k: v.strip() if isinstance(v, str) else v 
                     for k, v in row.items() if k != "Japanese_Name"}

            columns[key] = value

    with open(json_output_path, mode='w', encoding='utf-8') as out:
        json.dump({"columns": columns}, out, ensure_ascii=False, indent=4)

    print(f"Saved dictionary to {json_output_path}")


# Example usage
csv_to_dict("production_table_details.csv", "PRODUCTION_output.json")
