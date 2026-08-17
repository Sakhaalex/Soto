# File Operations Co-pilot Documentation & Ledger

This document lists the implemented features and architectural details of the **File Operations Co-pilot** system inside the SOTO Integration Hub.

## Target Audience
This ledger is prepared for future AI agents or developer handovers to ensure continuation of features without functional regressions.

---

## 1. Feature Specifications

### 📂 Directory & Target Manager
- **Feature**: Dynamic management of index target directories.
- **Backend API**: `browse_folder`, `get_targets`, `remove_target` actions in `copilot_server.py`.
- **UI Integration**: Clicking "➕ Add Folder" triggers a native Windows Folder Dialog (`tkinter.filedialog.askdirectory`), completely eliminating the need to copy-paste paths manually. Targets list is persisted in `targets.json` and dynamically rendered.

### 🔍 Deterministic Fast Search & Preview
- **Feature**: Real-time search by filename, extension, or path queries.
- **UI Integration**: Centered prominent blue search bar at the top, rendering matching files instantaneously with distinct visual cards and specialized file-type emojis.
- **Limit Handling**: Grid display is capped at 100 entries for rendering efficiency, with stats showing the total count of matches.

### 📊 File Stats & Extension Breakdown
- **Feature**: Analysis of file count distributions.
- **UI Integration**: Displays total tracked files, total folders, and a dynamic list of top file extension tags. Clicking any extension tag instantly filters search results by that extension.

### 🛠️ Folder Tree Cloning
- **Feature**: Instantly recreate an empty folder skeleton at a destination folder.
- **Backend API**: `recreate_structure` in `copilot_server.py` walks the directory structure and replicates subfolders at the target destination without duplicating the files.

### 📦 Advanced Segregation & File Sorting
- **Feature**: Sort messy directories based on custom parameters.
- **Backend API**: `segregate_advanced` in `copilot_server.py` allows moving files from a source folder to a destination path based on:
  1. **Extension** (e.g. `.pdf`, `.docx`)
  2. **Size** (e.g. moving files larger than a specified Megabytes limit)
  3. **Age** (e.g. moving files older than a specified number of days)

### 🖥️ Native OS Integration (Actions)
- **Feature**: Interacting directly with the local file system.
- **Backend API**: 
  - `open_file`: Launches the file in its default program.
  - `open_folder`: Highlights the file inside the Windows File Explorer (`explorer.exe /select, ...`).

### ⚙️ Dynamic Server Auto-Binding
- **Feature**: Dynamic host port selection.
- **Backend API**: Binds to port `0` (system-allocated free port) to eliminate port conflicts entirely. Launches Brave/default browser automatically, pointing to the active instance.

---

## 2. Ledger of Files

- **[file_indexer.py](file:///x:/Alexander/Cabin/Projects/Programming/Soto/File/file_indexer.py)**: Scans directories, handles folder ordering (folders at the end prefixed with `*`), chains overflow rows beyond limit, and marks deleted items with time-logs.
- **[copilot_server.py](file:///x:/Alexander/Cabin/Projects/Programming/Soto/File/copilot_server.py)**: Dynamic python server serving API endpoints and handling OS native commands (Open, Show in Folder, tkinter dialogs).
- **[file_copilot.html](file:///x:/Alexander/Cabin/Projects/Programming/Soto/File/file_copilot.html)**: Front-end dashboard featuring the search controls, stats panel, target directory management, advanced segregation, and structural cloning interface.
- **[targets.json](file:///x:/Alexander/Cabin/Projects/Programming/Soto/File/targets.json)**: Stores target folder paths.
