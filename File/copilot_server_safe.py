import os
import shutil
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse
import subprocess
import webbrowser
import socket
import tkinter as tk
from tkinter import filedialog

class CopilotHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))
        
        action = payload.get("action")
        response_data = {"status": "success"}
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        targets_json_path = os.path.join(script_dir, "targets.json")

        try:
            if action == "open_file":
                target_path = payload.get("path")
                if os.path.exists(target_path):
                    os.startfile(target_path)
                else:
                    response_data = {"status": "error", "msg": f"File not found: {target_path}"}
                    
            elif action == "open_folder":
                target_path = payload.get("path")
                if os.path.exists(target_path):
                    # Select file/folder in Explorer
                    subprocess.run(['explorer', '/select,', os.path.normpath(target_path)])
                else:
                    response_data = {"status": "error", "msg": f"Folder/file not found: {target_path}"}

            elif action == "get_targets":
                if os.path.exists(targets_json_path):
                    with open(targets_json_path, 'r', encoding='utf-8') as f:
                        response_data["targets"] = json.load(f)
                else:
                    response_data["targets"] = []

            elif action == "browse_folder":
                # Run folder dialog in separate process to avoid thread hangs and blockages
                cmd = ["python", "-c", "import tkinter as tk; from tkinter import filedialog; root=tk.Tk(); root.withdraw(); root.attributes('-topmost', True); print(filedialog.askdirectory(title='Select Folder to Index'))"]
                try:
                    selected_dir = subprocess.check_output(cmd).decode('utf-8', errors='replace').strip()
                except Exception as ex:
                    print(f"Subprocess folder dialog failed: {ex}")
                    selected_dir = ""
                
                if selected_dir and os.path.exists(selected_dir):
                    selected_dir = os.path.normpath(selected_dir)
                    targets = []
                    if os.path.exists(targets_json_path):
                        with open(targets_json_path, 'r', encoding='utf-8') as f:
                            targets = json.load(f)
                    if selected_dir not in targets:
                        targets.append(selected_dir)
                        with open(targets_json_path, 'w', encoding='utf-8') as f:
                            json.dump(targets, f, indent=4)
                    response_data["path"] = selected_dir
                else:
                    response_data["status"] = "cancelled"

            elif action == "add_target":
                target_path = payload.get("path")
                if target_path:
                    target_path = os.path.normpath(target_path.strip())
                    if os.path.exists(target_path):
                        targets = []
                        if os.path.exists(targets_json_path):
                            with open(targets_json_path, 'r', encoding='utf-8') as f:
                                targets = json.load(f)
                        if target_path not in targets:
                            targets.append(target_path)
                            with open(targets_json_path, 'w', encoding='utf-8') as f:
                                json.dump(targets, f, indent=4)
                        response_data["targets"] = targets
                    else:
                        response_data = {"status": "error", "msg": f"Path does not exist on disk: {target_path}"}
                else:
                    response_data = {"status": "error", "msg": "No path provided."}

            elif action == "remove_target":
                target_path = payload.get("path")
                if os.path.exists(targets_json_path):
                    with open(targets_json_path, 'r', encoding='utf-8') as f:
                        targets = json.load(f)
                    normalized_target = os.path.normpath(target_path)
                    targets = [os.path.normpath(t) for t in targets]
                    if normalized_target in targets:
                        targets.remove(normalized_target)
                        with open(targets_json_path, 'w', encoding='utf-8') as f:
                            json.dump(targets, f, indent=4)
                
            elif action == "segregate_extension":
                src_dir = payload.get("path")
                ext = payload.get("ext")
                if os.path.exists(src_dir):
                    dest_dir = os.path.join(src_dir, f"{ext.replace('.','').upper()}_Files")
                    os.makedirs(dest_dir, exist_ok=True)
                    for item in os.listdir(src_dir):
                        if item.lower().endswith(ext.lower()):
                            shutil.move(os.path.join(src_dir, item), os.path.join(dest_dir, item))

            elif action == "segregate_advanced":
                src_dir = payload.get("src_path")
                dest_dir = payload.get("dest_path")
                rule_type = payload.get("rule_type")
                rule_value = payload.get("rule_value")
                
                if os.path.exists(src_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                    moved_count = 0
                    import time
                    now = time.time()
                    
                    for item in os.listdir(src_dir):
                        item_path = os.path.join(src_dir, item)
                        if os.path.isdir(item_path):
                            continue
                            
                        should_move = False
                        if rule_type == 'extension':
                            if item.lower().endswith(rule_value.lower()):
                                should_move = True
                        elif rule_type == 'size':
                            try:
                                min_size = float(rule_value) * 1024 * 1024
                                if os.path.getsize(item_path) >= min_size:
                                    should_move = True
                            except:
                                pass
                        elif rule_type == 'date':
                            try:
                                min_age_seconds = float(rule_value) * 24 * 3600
                                if (now - os.path.getmtime(item_path)) >= min_age_seconds:
                                    should_move = True
                            except:
                                pass
                                
                        if should_move:
                            shutil.move(item_path, os.path.join(dest_dir, item))
                            moved_count += 1
                    response_data["msg"] = f"Moved {moved_count} files."
                else:
                    response_data = {"status": "error", "msg": "Source path does not exist."}

            elif action == "recreate_structure":
                src_dir = payload.get("src_path")
                dest_dir = payload.get("dest_path")
                if os.path.exists(src_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                    created_count = 0
                    for root_dir, dirs, files in os.walk(src_dir):
                        rel_path = os.path.relpath(root_dir, src_dir)
                        if rel_path == ".":
                            continue
                        target_dir = os.path.join(dest_dir, rel_path)
                        os.makedirs(target_dir, exist_ok=True)
                        created_count += 1
                    response_data["msg"] = f"Recreated {created_count} subfolders."
                else:
                    response_data = {"status": "error", "msg": "Source path does not exist."}
            
            elif action == "update_index":
                # Triggers the indexer
                import sys
                subprocess.run([sys.executable, os.path.join(script_dir, "file_indexer.py")])
                
        except Exception as e:
            response_data = {"status": "error", "msg": str(e)}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

if __name__ == "__main__":
    # Serve on port 0 to dynamically find an available port, avoiding conflicts
    server = HTTPServer(('localhost', 0), CopilotHandler)
    port = server.server_address[1]
    
    # Write server_config.js
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "server_config.js")
    try:
        with open(config_path, 'w', encoding='utf-8') as cf:
            cf.write(f"window.SOTO_SERVER_URL = 'http://localhost:{port}';\n")
    except Exception as e:
        print(f"Error writing server_config.js: {e}")

    url = f"http://localhost:{port}/file_copilot.html"
    print(f"File Operations Co-pilot Server started dynamically on port {port}")
    print(f"Launching default browser at {url}")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")