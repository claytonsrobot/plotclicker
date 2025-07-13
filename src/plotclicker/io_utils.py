import csv
import json
import os
from collections import defaultdict

def find_columns(header, x_match="time", y_match="force"):
    x_col = y_col = None
    for col in header:
        lc = col.lower()
        if x_col is None and x_match in lc:
            x_col = col
        if y_col is None and y_match in lc:
            y_col = col
    return x_col, y_col

def load_csv_data(filename, x_match="time", y_match="force"):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        x_col, y_col = find_columns(header, x_match, y_match)
        if not x_col or not y_col:
            raise ValueError(f"Could not identify X/Y columns in {filename}.")

        data = defaultdict(list)
        for row in reader:
            try:
                x = float(row[x_col])
                y = float(row[y_col])
                data['x'].append(x)
                data['y'].append(y)
                data['row'].append(row)
            except ValueError:
                continue
    return data, x_col, y_col

def save_selected_data(selected_points, all_data, x_col, y_col, raw_filename):
    from uuid import uuid4
    x_all = all_data['x']
    y_all = all_data['y']
    rows = all_data['row']

    def closest(xc, yc):
        return min(
            range(len(x_all)),
            key=lambda i: (x_all[i] - xc) ** 2 + (y_all[i] - yc) ** 2
        )

    kept_rows = [rows[closest(x, y)] for (x, y) in selected_points]
    assessed_id = str(uuid4())[:8]
    assessed_filename = f"{os.path.splitext(raw_filename)[0]}__assessed_{assessed_id}.csv"

    with open(assessed_filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(kept_rows)

    return assessed_filename, assessed_id

def update_json_register(json_path, entry):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            register = json.load(f)
    else:
        register = []
    register.append(entry)
    with open(json_path, 'w') as f:
        json.dump(register, f, indent=2)

def read_file_list(path):
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]
    