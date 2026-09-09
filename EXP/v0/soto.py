import csv

def read_csv_all(file_path):
    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        parameters = reader.fieldnames
        rows = [row for row in reader]
    return parameters, rows

def get_row_data(rows, row_index):
    if 0 <= row_index < len(rows):
        return rows[row_index]
    return None