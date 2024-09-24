import csv
import json

def save_to_csv(data, file_name="data.csv"):
    """Lưu tiêu đề vào file CSV."""
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title'])
        for title in data:
            writer.writerow([title])

def save_to_json(data, file_name="data.json"):
    """Lưu tiêu đề vào file JSON."""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump({"titles": data}, file, ensure_ascii=False, indent=4)
