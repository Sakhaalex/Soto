import os
import csv
import json
import time
from datetime import datetime

class FileIndexer:
    def __init__(self, output_file="File.csv", row_limit=999999):
        # Resolve path relative to this script's directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(self.script_dir, output_file)
        self.row_limit = row_limit
        self.previous_data = self._load_previous_scan()
        
    def _load_previous_scan(self):
        """Loads the previous File.csv to detect deleted items."""
        old_data = {}
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8', errors='replace') as f:
                    reader = csv.reader(f)
                    headers = next(reader, [])
                    for row in reader:
                        if len(row) >= 2 and row[0] != "CHN":
                            path = row[0]
                            items = [item for item in row[2:] if item]
                            old_data[path] = items
            except Exception as e:
                print(f"[INDEXER] Warning loading previous scan: {e}")
        return old_data

    def scan(self, target_dirs):
        records = []
        max_items = 0
        current_time = datetime.now().strftime("%Y%m%d_%H%M")
        
        for root_target in target_dirs:
            if not os.path.exists(root_target):
                continue

            for current_path, dirnames, filenames in os.walk(root_target):
                folder_name = os.path.basename(current_path) or current_path
                current_items = list(filenames)
                current_items.extend([f"*{d}" for d in dirnames])
                
                # Check for deleted files from previous scan
                if current_path in self.previous_data:
                    old_items = self.previous_data[current_path]
                    for old_item in old_items:
                        if old_item not in current_items and not old_item.startswith("[DELETED"):
                            # Mark as deleted with timestamp
                            deleted_marker = f"[DELETED_{current_time}]_{old_item}"
                            current_items.append(deleted_marker)

                if len(current_items) > max_items:
                    max_items = len(current_items)

                records.append({
                    "Path": current_path,
                    "Folder": folder_name,
                    "Items": current_items
                })

        self._write_csv(records, max_items)
        self._write_js(records)

    def _write_js(self, records):
        js_file = os.path.join(self.script_dir, "file_data.js")
        items_list = []
        for rec in records:
            basePath = rec["Path"]
            for item in rec["Items"]:
                is_deleted = item.startswith("[DELETED")
                is_folder = item.startswith("*")
                name = item[1:] if is_folder else (item.split(']_')[1] if is_deleted else item)
                ext = 'folder' if is_folder else ('.' + name.split('.')[-1].lower() if '.' in name else '')
                items_list.append({
                    "name": name,
                    "path": basePath + "\\" + name,
                    "parent": basePath,
                    "isFolder": is_folder,
                    "isDeleted": is_deleted,
                    "ext": ext
                })
        
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write("window.sotoFileData = " + json.dumps(items_list, indent=2) + ";\n")
        print(f"[INDEXER] Successfully wrote file_data.js with {len(items_list)} items.")

    def _write_csv(self, records, max_items):
        headers = ["Path", "Folder"] + [f"F{i+1}" for i in range(max_items)]
        
        file_index = 1
        current_file = self.output_file
        row_count = 0
        
        f = open(current_file, 'w', newline='', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for rec in records:
            if row_count >= self.row_limit:
                # Chain to next CSV
                next_file = self.output_file.replace(".csv", f"_{file_index + 1}.csv")
                writer.writerow(["CHN", next_file])
                f.close()
                
                file_index += 1
                current_file = next_file
                f = open(current_file, 'w', newline='', encoding='utf-8')
                writer = csv.writer(f)
                writer.writerow(headers)
                row_count = 0

            row = [rec["Path"], rec["Folder"]] + rec["Items"]
            row += [""] * (len(headers) - len(row))
            writer.writerow(row)
            row_count += 1
            
        f.close()
        print(f"[INDEXER] Successfully mapped {len(records)} directories.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    targets_json_path = os.path.join(script_dir, "targets.json")
    
    if os.path.exists(targets_json_path):
        try:
            with open(targets_json_path, 'r', encoding='utf-8') as tj:
                targets = json.load(tj)
        except Exception as e:
            print(f"[INDEXER] Error reading targets.json: {e}")
            targets = []
    else:
        user_home = os.path.expanduser("~")
        targets = [os.path.join(user_home, "Downloads"), os.path.join(user_home, "Documents")]
        with open(targets_json_path, 'w', encoding='utf-8') as tj:
            json.dump(targets, tj, indent=4)
    
    indexer = FileIndexer("File.csv")
    indexer.scan(targets)