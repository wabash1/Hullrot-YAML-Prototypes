import os
import yaml

OUTPUT_FILE = "airlock_ids.txt"

def extract_airlock_ids(data, parent_key=""):
    """ Recursively search for 'id' fields in a YAML structure where 'id' contains 'Airlock' or the parent key contains 'Airlock'. """
    found_ids = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower() == "id" and isinstance(value, str) and "airlock" in value.lower():
                found_ids.append(value)  # Capture the actual ID value
            elif "airlock" in key.lower():
                if isinstance(value, dict) and "id" in value and isinstance(value["id"], str):
                    found_ids.append(value["id"])  # Capture ID inside a parent containing "Airlock"
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "id" in item and isinstance(item["id"], str):
                            found_ids.append(item["id"])  # Capture IDs inside lists
            else:
                found_ids.extend(extract_airlock_ids(value, key))
    
    elif isinstance(data, list):
        for item in data:
            found_ids.extend(extract_airlock_ids(item, parent_key))
    
    return found_ids

def scan_folder_for_yaml(folder):
    """ Recursively scans a folder for YAML files and extracts relevant 'id' values. """
    airlock_ids = []
    
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith((".yml", ".yaml")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        yaml_data = yaml.safe_load(f)
                        if yaml_data:
                            ids = extract_airlock_ids(yaml_data)
                            if ids:
                                airlock_ids.extend(ids)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return airlock_ids

def save_to_file(ids, output_file):
    """ Saves the extracted IDs to a text file in the format '- {actual_id}' """
    with open(output_file, "w", encoding="utf-8") as f:
        for rid in ids:
            f.write(f"- {rid}\n")  # Write the actual ID value
    print(f"\nIDs saved to {output_file}")

if __name__ == "__main__":
    current_folder = os.getcwd()
    print(f"Scanning folder: {current_folder} for YAML files...\n")
    
    result_ids = scan_folder_for_yaml(current_folder)

    if result_ids:
        save_to_file(result_ids, OUTPUT_FILE)
    else:
        print("\nNo matching IDs found.")
