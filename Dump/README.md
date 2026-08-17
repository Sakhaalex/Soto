Soto — quick tools

To convert all Markdown syllabus files in this workspace into a single `Record.csv`, run:

```bash
python scripts/md_to_csv.py
```

The script will look for `*.md` files in the repo root, parse course/unit/CO/lab heuristically, and write `Record.csv` at the workspace root. You can then open `dist/soto_viewer.html` or load `Record.csv` into the main app.
