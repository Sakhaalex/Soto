
### 1. CSV is the single source of truth



There should be one authoritative index:



`File.csv`



Potentially followed by:



`File_2.csv`, `File_3.csv`, etc. only when the CSV row limit is reached.



No `targets.json` should be required for the indexing model.



The target folders themselves should be represented in `File.csv`.



### 2. Add Target Folder



When the user clicks:



`+ ADD FOLDER`



the program opens the Windows folder browser.



Suppose the user selects:



`D:\Projects`



The system should immediately make `D:\Projects` an indexed root.



It should then scan:



`D:\Projects`

→ files

→ folders

→ subfolders

→ files inside subfolders

→ deeper subfolders

→ etc.



The complete hierarchy becomes part of `File.csv`.



### 3. Folder hierarchy representation



Your original idea is essentially a lightweight filesystem graph represented using CSV.



For example:



```text

Path                         Folder       F1          F2          F3

D:\Projects                  Projects     main.py     README.md   *src

D:\Projects\src              src          test.py     *utils

D:\Projects\src\utils        utils        helper.py

```



The important rule is:



`*folder_name`



means that the item is a folder and therefore points to another `Path` row.



Files remain unchanged:



```text

main.py

README.md

test.py

```



Folders become:



```text

*src

*utils

```



And folders are always placed after files within the same row.



This is one of the central design decisions of the project.



### 4. Initial indexing



The first time a target is added:



```text

ADD FOLDER

      ↓

Select folder

      ↓

Scan complete hierarchy

      ↓

Create/update File.csv

```



The system should not merely record the selected folder.



It must actually index everything underneath it.



### 5. Update / Rescan



This is where the current implementation is conceptually incomplete.



When the user presses:



`UPDATE`



the system should NOT blindly recreate the entire CSV from scratch.



Instead, conceptually:



```text

Existing File.csv

        ↓

Read existing indexed paths

        ↓

Check those paths on disk

        ↓

Detect:

    new files

    deleted files

    new folders

    deleted folders

    renamed/moved items

        ↓

Update File.csv

```



The filesystem is the external state.



`File.csv` is the recorded index of that state.



So the update operation reconciles:



```text

REAL FILESYSTEM

       ↕

   File.csv

```



That distinction is important.



### 6. New files



Suppose the CSV currently contains:



```text

D:\Projects\src    src    test.py    *utils

```



and someone creates:



```text

D:\Projects\src    src    test.py    new.py    *utils

```



After UPDATE:



```text

D:\Projects\src    src    test.py    new.py    *utils

```



The new file is incorporated.



### 7. New folders



If:



```text

D:\Projects\src\new_folder

```



is created, UPDATE should discover it and create its corresponding `Path` record.



For example:



```text

D:\Projects\src

D:\Projects\src\new_folder

```



The parent row contains:



```text

*new_folder

```



### 8. Deleted files



Your original requirement is stronger than simply removing deleted files.



If:



```text

report.pdf

```



was previously indexed and subsequently deleted, the CSV should retain evidence of the deletion.



Something along the lines of:



```text

[DELETED_20260817_1530]_report.pdf

```



This gives you a basic historical ledger.



I would preserve this behaviour, but later we should define exactly how deleted folders are represented because deleting a folder can imply hundreds of deleted descendants.



### 9. File/folder distinction



The `*` convention should remain.



It is simple and fits your CSV-oriented design:



```text

F1    report.pdf

F2    image.png

F3    *Documents

F4    *Projects

```



No additional database field is necessary just to identify folders.



### 10. Search



The browser GUI should search the CSV-derived index.



Search should eventually support:



```text

filename

folder

extension

path

```



For example:



`report`



could find:



```text

report.pdf

monthly_report.docx

report_backup.zip

```



### 11. Extension statistics



Because the index already knows filenames, the system can derive:



```text

.pdf     428

.docx    152

.py       93

.jpg     731

.mp4     204

```



This should be generated from the CSV/index rather than maintained separately.



### 12. File information



Selecting a file can show information such as:



```text

Name

Extension

Full Path

Parent Folder

Size

Created

Modified

```



This does not necessarily need to be permanently stored in `File.csv`.



The CSV can remain lightweight while the GUI obtains detailed metadata from the OS when requested.



That is closer to your original intention.



### 13. Open file



Clicking a result should allow:



`OPEN`



which launches the file using the operating system's default application.



### 14. Show in folder



Another operation:



`SHOW IN FOLDER`



should open Windows Explorer and highlight the selected file.



The current `copilot_server.py` already attempts this with Explorer. 



### 15. Directory tree



The GUI should be able to construct a visual tree from:



```text

Path

+

*folder references

```



For example:



```text

D:

└── Projects

    ├── README.md

    ├── main.py

    ├── src

    │   ├── test.py

    │   └── utils

    │       └── helper.py

    └── assets

        └── image.png

```



This is a visual representation of the CSV, not a second source of truth.



### 16. Folder structure cloning



Because the CSV contains every folder path, the program can reconstruct only the directories.



Example:



```text

Original

D:\Projects

├── src

│   └── utils

├── assets

└── documentation

```



Clone to:



```text

E:\Backup

├── src

│   └── utils

├── assets

└── documentation

```



No files need to be copied.



### 17. File segregation



This is a separate operational feature.



Example:



```text

Downloads

├── a.pdf

├── b.pdf

├── c.docx

├── d.jpg

└── e.png

```



The system could create:



```text

Downloads

├── PDF

│   ├── a.pdf

│   └── b.pdf

├── DOCX

│   └── c.docx

└── IMAGE

    ├── d.jpg

    └── e.png

```



Your current server already has an extension segregation implementation. 



### 18. Advanced segregation



Later, the same mechanism can operate on:



```text

Extension

Size

Age / modified date

```



For example:



```text

Move files > 500 MB

Move files older than 180 days

Move all PDFs

```



The current implementation has these three rule types, although they currently operate directly on the filesystem rather than being driven by the CSV index. 



### 19. Target management



This is where I would change the current design significantly.



Currently:



```text

targets.json

     ↓

target folders

```



The current server explicitly reads and writes `targets.json` for `get_targets`, `add_target`, `remove_target`, and folder browsing. 



Your intended model appears to be:



```text

File.csv

   ↓

Indexed root paths

   ↓

Complete hierarchy

```



Therefore, target management should eventually derive its information from `File.csv`.



### 20. Automatic update



Your original idea has two update triggers:



```text

MANUAL

   UPDATE button

```



and eventually:



```text

SYSTEM STARTUP

   ↓

AX File Operations

   ↓

UPDATE INDEX

```



I would keep startup indexing as a future feature rather than making it part of the first stable version.



### 21. CSV chaining



Your `CHN` idea is valid.



For example:



```text

File.csv

     ↓

reaches limit

     ↓

CHN | File_2.csv

```



then:



```text

File_2.csv

     ↓

CHN | File_3.csv

```



The application treats them as one logical index.



This is particularly important because the CSV format itself has a practical spreadsheet row limit. Don't create anything on repo


