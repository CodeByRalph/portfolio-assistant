import json
import glob
import os
import pandas as pd

# Loading Data
DATA_PATH = 'Data/json'


def get_file_list():
    files_to_merge = []
    file_path = glob.glob(os.path.join(DATA_PATH, '*.json'))
    for file in file_path:
        files_to_merge.append(file)
    return files_to_merge


def remove_nulls_from_file(input_file, output_file):
    def remove_nulls(obj):
        if isinstance(obj, dict):
            return {k: remove_nulls(v) for k, v in obj.items() if v is not None}
        elif isinstance(obj, list):
            return [remove_nulls(i) for i in obj if i is not None]
        else:
            return obj

    with open(input_file, 'r') as infile:
        data = [json.loads(line) for line in infile]

    cleaned_data = [remove_nulls(item) for item in data]

    with open(output_file, 'w') as outfile:
        for item in cleaned_data:
            json.dump(item, outfile)
            outfile.write('\n')


def merge_files():
    files = get_file_list()
    combined_data = []
    for file in files:
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                combined_data.append(data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {file}")

    # Flatten the combined data if it's a list of lists or dicts
    flat_data = []
    for item in combined_data:
        if isinstance(item, list):
            flat_data.extend(item)
        else:
            flat_data.append(item)

    # Create a DataFrame from the flattened data
    combined_df = pd.json_normalize(flat_data)
    combined_df.to_json(f'{DATA_PATH}/combined.json', orient='records', lines=True)
    remove_nulls_from_file(f'{DATA_PATH}/combined.json', f'{DATA_PATH}/combined_cleaned.json')



merge_files()