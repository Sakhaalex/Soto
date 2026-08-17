from __future__ import annotations

import os
import random
import shutil
import subprocess
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import customtkinter as ctk

from File.file_indexer import FileIndexer


APP_TITLE = "Automation Drive"

BG = "#0b0f14"
PANEL = "#11161d"
PANEL_2 = "#171d26"
SURFACE = "#f6f7fb"
TEXT = "#f3f4f6"
TEXT_DARK = "#0f172a"
MUTED = "#94a3b8"
ORANGE = "#f97316"
SKY = "#38bdf8"
WHITE = "#ffffff"
GRAY = "#cbd5e1"
LINE = "#263041"


THOUGHTS = [
    "file operations",
    "source of truth",
    "search",
    "clone structure",
    "segregation",
    "extensions",
    "folder tree",
    "update index",
    "show in folder",
    "automation drive",
    "csv first",
    "native app",
    "future modules",
    "metadata",
    "launchers",
    "structure clone",
]


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def normalize_path(value: str) -> str:
    return os.path.normpath(os.path.abspath(os.path.expanduser(str(value))))


def split_deleted_name(item: str) -> str:
    if item.startswith("[DELETED_"):
        closing = item.find("]_")
        if closing != -1:
            return item[closing + 2 :]
    parts = item.split("_", 3)
    if len(parts) == 4:
        return parts[3]
    return item


def nice_ext(name: str, is_folder: bool) -> str:
    if is_folder:
        return "folder"
    if "." in name:
        return "." + name.rsplit(".", 1)[1].lower()
    return "no extension"


class ThoughtWall(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG, **kwargs)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.lines = []
        self.after_id = None
        self.bind("<Configure>", self._restart)

    def _restart(self, _event=None):
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.canvas.delete("all")
        self.lines.clear()
        self._build()
        self._tick()

    def _build(self):
        width = max(self.winfo_width(), 600)
        height = max(self.winfo_height(), 360)
        lane_count = 10
        spacing = height // (lane_count + 1)
        choices = THOUGHTS[:]
        random.shuffle(choices)

        for lane in range(lane_count):
            y = spacing * (lane + 1)
            lane_items = []
            x = random.randint(-200, 50)
            labels = random.sample(choices, k=min(8, len(choices)))
            for idx in range(2):
                for word in labels:
                    item = self.canvas.create_text(
                        x,
                        y,
                        text=word.upper(),
                        fill="#8f99a8",
                        font=("Segoe UI", 10, "bold"),
                        anchor="w",
                    )
                    bbox = self.canvas.bbox(item)
                    width_text = (bbox[2] - bbox[0]) if bbox else len(word) * 8 + 24
                    lane_items.append((item, width_text))
                    x += width_text + 48
            self.lines.append({"items": lane_items, "y": y})

    def _tick(self):
        width = max(self.winfo_width(), 600)
        for lane in self.lines:
            for item, item_width in lane["items"]:
                self.canvas.move(item, -0.7, 0)
                x1, _, x2, _ = self.canvas.bbox(item) or (0, 0, 0, 0)
                if x2 < -20:
                    self.canvas.move(item, width + 240, 0)
        self.after_id = self.after(35, self._tick)


class LauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title(APP_TITLE)
        self.geometry("1450x900")
        self.minsize(1260, 780)
        self.configure(fg_color=BG)

        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        nav = ctk.CTkFrame(self, fg_color="#070a0f", corner_radius=0, height=64)
        nav.grid(row=0, column=0, sticky="ew")
        nav.grid_propagate(False)
        nav.grid_columnconfigure(1, weight=1)

        brand = ctk.CTkFrame(nav, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="w", padx=18, pady=12)
        ctk.CTkLabel(brand, text="AUTOMATION", text_color=WHITE, font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        ctk.CTkLabel(brand, text=".", text_color=ORANGE, font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        ctk.CTkLabel(brand, text="DRIVE", text_color=WHITE, font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        nav_right = ctk.CTkFrame(nav, fg_color="transparent")
        nav_right.grid(row=0, column=2, sticky="e", padx=18)
        ctk.CTkLabel(nav_right, text="READY", text_color=ORANGE, font=ctk.CTkFont(size=11, weight="bold")).pack(side="right", padx=8)
        ctk.CTkButton(nav_right, text="Open File Ops", fg_color=SKY, hover_color="#0ea5e9", text_color=TEXT_DARK, height=30, corner_radius=10, command=self.open_file_ops).pack(side="right", padx=8)

        body = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=7)
        body.grid_columnconfigure(1, weight=5)
        body.grid_rowconfigure(0, weight=1)

        self.wall = ThoughtWall(body)
        self.wall.grid(row=0, column=0, sticky="nsew")

        right = ctk.CTkFrame(body, fg_color=BG, corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew", padx=(0, 18), pady=(0, 18))
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        hero = ctk.CTkFrame(right, fg_color=PANEL, corner_radius=22)
        hero.grid(row=0, column=0, sticky="ew", pady=(18, 14))
        hero.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(hero, text="Automation Drive", text_color=WHITE, font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w", padx=20, pady=(18, 4))
        ctk.CTkLabel(hero, text="A native shell for files, future automations, and clean system tools.", text_color=GRAY, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)

        chip_row = ctk.CTkFrame(hero, fg_color="transparent")
        chip_row.pack(anchor="w", padx=20, pady=14)
        for label, color in [("CSV First", ORANGE), ("Native App", SKY), ("Expandable", "#64748b")]:
            ctk.CTkLabel(chip_row, text=label, fg_color=color, text_color=TEXT_DARK, corner_radius=999, padx=10, pady=5, font=ctk.CTkFont(size=10, weight="bold")).pack(side="left", padx=(0, 8))

        ctk.CTkButton(hero, text="Launch Workspace", fg_color=WHITE, text_color=TEXT_DARK, hover_color="#e2e8f0", height=42, corner_radius=14, font=ctk.CTkFont(size=13, weight="bold"), command=self.open_file_ops).pack(anchor="w", padx=20, pady=(0, 18))

        projects = ctk.CTkFrame(right, fg_color=PANEL, corner_radius=22)
        projects.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        projects.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(projects, text="Projects", text_color=WHITE, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(18, 10))

        self._project_card(projects, "File Operations", "Sky blue workspace for search, indexing, and file actions.", SKY, self.open_file_ops)
        self._project_card(projects, "Future Modules", "Reserve space for new automation systems without changing the launcher.", ORANGE, None, disabled=True)
        self._project_card(projects, "Documentation", "Release notes, design decisions, and the CSV model.", "#64748b", self.open_docs)

        footer = ctk.CTkFrame(self, fg_color="#070a0f", corner_radius=0, height=40)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        ctk.CTkLabel(footer, text="Automation Drive • first release launcher", text_color="#8b97a8", font=ctk.CTkFont(size=10)).pack(side="left", padx=16, pady=10)

    def _project_card(self, parent, title, desc, color, command, disabled=False):
        card = ctk.CTkFrame(parent, fg_color="#0f172a", corner_radius=16)
        card.pack(fill="x", padx=16, pady=8)
        left = ctk.CTkFrame(card, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=16, pady=14)
        ctk.CTkLabel(left, text=title, text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(left, text=desc, text_color=MUTED, font=ctk.CTkFont(size=11), wraplength=360, justify="left").pack(anchor="w", pady=(4, 0))
        btn = ctk.CTkButton(
            card,
            text="Open",
            fg_color=color if not disabled else "#334155",
            hover_color="#0ea5e9" if color == SKY else "#ea580c" if color == ORANGE else "#475569",
            text_color=TEXT_DARK if color == SKY else WHITE,
            corner_radius=12,
            height=34,
            width=90,
            command=command if command and not disabled else lambda: None,
            state="normal" if not disabled else "disabled",
        )
        btn.pack(side="right", padx=16, pady=16)

    def open_file_ops(self):
        if hasattr(self, "_file_ops") and self._file_ops.winfo_exists():
            self._file_ops.focus()
            return
        self._file_ops = FileOpsWindow(self)

    def open_docs(self):
        docs = self.base_dir / "File" / "documentation.md"
        try:
            os.startfile(str(docs))
        except Exception as error:
            messagebox.showerror(APP_TITLE, str(error))


class FileOpsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("File Operations")
        self.geometry("1320x840")
        self.minsize(1180, 720)
        self.configure(fg_color=BG)
        self.transient(master)

        self.indexer = FileIndexer("File.csv")
        self.records = []
        self.items = []
        self.targets = []
        self.current_path = ""

        self._build_ui()
        self.reload_index()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="#070a0f", corner_radius=0, height=74)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=16, pady=12)
        ctk.CTkLabel(left, text="FILE OPERATIONS", text_color=WHITE, font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(left, text="Sky blue tools on a black, gray, white, and orange shell.", text_color="#9aa4b2", font=ctk.CTkFont(size=11)).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e", padx=16)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.filter_items())
        search = ctk.CTkEntry(right, textvariable=self.search_var, width=420, height=38, corner_radius=12, placeholder_text="Search files, folders, paths, extensions...")
        search.pack(side="left", padx=(0, 10))
        ctk.CTkButton(right, text="Add Folder", fg_color=SKY, hover_color="#0ea5e9", text_color=TEXT_DARK, height=38, corner_radius=12, command=self.add_folder).pack(side="left", padx=5)
        ctk.CTkButton(right, text="Update", fg_color=ORANGE, hover_color="#ea580c", height=38, corner_radius=12, command=self.update_index).pack(side="left", padx=5)
        ctk.CTkButton(right, text="Refresh", fg_color="#334155", hover_color="#475569", height=38, corner_radius=12, command=self.reload_index).pack(side="left", padx=5)

        body = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        body.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, weight=0)
        body.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=20, width=260)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        self.sidebar.grid_propagate(False)
        self.main = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=20)
        self.main.grid(row=0, column=1, sticky="nsew", padx=(0, 14))
        self.details = ctk.CTkFrame(body, fg_color=PANEL, corner_radius=20, width=300)
        self.details.grid(row=0, column=2, sticky="nsew")
        self.details.grid_propagate(False)

        self._build_sidebar()
        self._build_main()
        self._build_details()

        footer = ctk.CTkFrame(self, fg_color="#070a0f", corner_radius=0, height=34)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_propagate(False)
        self.status = ctk.CTkLabel(footer, text="Ready", text_color="#9aa4b2", font=ctk.CTkFont(size=10))
        self.status.pack(side="left", padx=16, pady=8)

    def _build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Targets", text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 8))
        self.targets_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", height=220)
        self.targets_frame.pack(fill="x", padx=14, pady=(0, 10))

        ctk.CTkLabel(self.sidebar, text="Stats", text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(6, 8))
        self.stat_folders = self._stat_row("Folders", "0")
        self.stat_items = self._stat_row("Items", "0")
        self.stat_live = self._stat_row("Live", "0")
        self.stat_deleted = self._stat_row("Deleted", "0")

        ctk.CTkLabel(self.sidebar, text="Quick Actions", text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(10, 8))
        self._side_btn("Open Selected", self.open_selected, "#334155")
        self._side_btn("Show in Folder", self.show_selected, "#334155")
        self._side_btn("Copy Path", self.copy_selected_path, "#334155")
        self._side_btn("Clone Structure", self.clone_structure_prompt, "#334155")
        self._side_btn("Segregate", self.segregate_prompt, "#334155")

    def _stat_row(self, label, value):
        row = ctk.CTkFrame(self.sidebar, fg_color="#0f172a", corner_radius=12)
        row.pack(fill="x", padx=14, pady=5)
        ctk.CTkLabel(row, text=label, text_color=MUTED, font=ctk.CTkFont(size=10)).pack(side="left", padx=12, pady=10)
        lbl = ctk.CTkLabel(row, text=value, text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold"))
        lbl.pack(side="right", padx=12)
        return lbl

    def _side_btn(self, text, command, color):
        ctk.CTkButton(self.sidebar, text=text, command=command, fg_color=color, hover_color="#475569", corner_radius=12, height=36).pack(fill="x", padx=14, pady=5)

    def _build_main(self):
        top = ctk.CTkFrame(self.main, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(14, 10))
        ctk.CTkLabel(top, text="Search Results", text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        self.count = ctk.CTkLabel(top, text="0 items", text_color=MUTED)
        self.count.pack(side="left", padx=10)

        actions = ctk.CTkFrame(self.main, fg_color="transparent")
        actions.pack(fill="x", padx=14, pady=(0, 10))
        for label, cmd, color in [
            ("Open", self.open_selected, SKY),
            ("Show", self.show_selected, ORANGE),
            ("Add Folder", self.add_folder, "#334155"),
        ]:
            ctk.CTkButton(actions, text=label, command=cmd, fg_color=color, hover_color="#0ea5e9" if color == SKY else "#ea580c" if color == ORANGE else "#475569", text_color=TEXT_DARK if color == SKY else WHITE, height=34, corner_radius=12).pack(side="left", padx=5)

        table = ctk.CTkFrame(self.main, fg_color="#0f172a", corner_radius=14)
        table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        cols = ("type", "name", "parent", "path", "status")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", style="Automation.Treeview")
        for col, head, width in [("type", "Type", 80), ("name", "Name", 190), ("parent", "Parent", 240), ("path", "Path", 400), ("status", "Status", 90)]:
            self.tree.heading(col, text=head)
            self.tree.column(col, width=width, anchor="w")
        scroll = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<Double-1>", lambda _e: self.open_selected())

    def _build_details(self):
        ctk.CTkLabel(self.details, text="Details", text_color=WHITE, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=14, pady=(14, 10))
        self.detail_labels = {}
        for key in ["Name", "Type", "Status", "Parent", "Path", "Extension"]:
            row = ctk.CTkFrame(self.details, fg_color="#0f172a", corner_radius=12)
            row.pack(fill="x", padx=14, pady=6)
            ctk.CTkLabel(row, text=key, text_color=MUTED, width=90, anchor="w").pack(side="left", padx=12, pady=10)
            lbl = ctk.CTkLabel(row, text="-", text_color=WHITE, anchor="w", justify="left")
            lbl.pack(side="left", fill="x", expand=True, padx=8, pady=10)
            self.detail_labels[key.lower()] = lbl

        self.clone_src = self._field("Clone Source")
        self.clone_dst = self._field("Clone Destination")
        ctk.CTkButton(self.details, text="Run Clone", fg_color="#334155", hover_color="#475569", corner_radius=12, height=34, command=self.clone_structure).pack(fill="x", padx=14, pady=(4, 8))
        self.seg_src = self._field("Segregate Source")
        self.seg_dst = self._field("Segregate Destination")
        self.seg_mode = ctk.CTkOptionMenu(self.details, values=["extension", "size", "age"], fg_color="#1f2937", button_color=SKY, button_hover_color="#0ea5e9")
        self.seg_mode.set("extension")
        self.seg_mode.pack(fill="x", padx=14, pady=6)
        self.seg_value = self._field("Rule Value")
        ctk.CTkButton(self.details, text="Run Segregation", fg_color=ORANGE, hover_color="#ea580c", corner_radius=12, height=34, command=self.segregate).pack(fill="x", padx=14, pady=(4, 14))

    def _field(self, placeholder):
        entry = ctk.CTkEntry(self.details, placeholder_text=placeholder)
        entry.pack(fill="x", padx=14, pady=6)
        return entry

    def set_status(self, text):
        self.status.configure(text=text)

    def reload_index(self):
        self.records = self.indexer._load_csv()
        self.targets = self.indexer._find_roots(self.records) if self.records else []
        self.items = self._build_items(self.records)
        self._render_targets()
        self._render_stats()
        self.filter_items()
        self.set_status(f"Loaded {len(self.records)} folders and {len(self.items)} items.")

    def _build_items(self, records):
        items = []
        for record in records:
            parent = normalize_path(record.get("Path", ""))
            for raw in record.get("Items", []):
                if not raw:
                    continue
                deleted = raw.startswith("[DELETED_") or raw.startswith("D_")
                folder = raw.startswith("*") and not deleted
                name = split_deleted_name(raw) if deleted else raw[1:] if folder else raw
                items.append(
                    {
                        "name": name,
                        "parent": parent,
                        "path": normalize_path(os.path.join(parent, name)),
                        "type": "Folder" if folder else "File",
                        "status": "Deleted" if deleted else "Live",
                        "ext": nice_ext(name, folder),
                        "isFolder": folder,
                        "isDeleted": deleted,
                    }
                )
        return items

    def _render_targets(self):
        for child in self.targets_frame.winfo_children():
            child.destroy()
        if not self.targets:
            ctk.CTkLabel(self.targets_frame, text="No targets indexed yet.", text_color=MUTED).pack(anchor="w", padx=4, pady=4)
            return
        for target in self.targets:
            ctk.CTkButton(self.targets_frame, text=target, fg_color="#0f172a", hover_color="#1e293b", corner_radius=10, height=32, anchor="w", command=lambda p=target: self.search_var.set(p)).pack(fill="x", pady=4)

    def _render_stats(self):
        self.stat_folders.configure(text=str(len(self.records)))
        self.stat_items.configure(text=str(len(self.items)))
        self.stat_live.configure(text=str(sum(1 for i in self.items if not i["isDeleted"] and not i["isFolder"])))
        self.stat_deleted.configure(text=str(sum(1 for i in self.items if i["isDeleted"])))

    def filter_items(self):
        query = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        self.visible = []
        for item in self.items:
            if not query or any(query in str(item[k]).lower() for k in ("name", "parent", "path", "ext", "type", "status")):
                self.visible.append(item)
        for item in self.visible[:1000]:
            self.tree.insert("", "end", values=(item["type"], item["name"], item["parent"], item["path"], item["status"]))
        self.count.configure(text=f"{len(self.visible)} items")
        self.set_status(f"Showing {min(len(self.visible), 1000)} of {len(self.visible)} matches.")

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if len(values) < 5:
            return
        data = {"type": values[0], "name": values[1], "parent": values[2], "path": values[3], "status": values[4], "ext": nice_ext(values[1], values[0] == "Folder")}
        self.current_path = data["path"]
        for key, label in self.detail_labels.items():
            label.configure(text=data.get(key, "-"))

    def _selected_path(self):
        if self.current_path:
            return self.current_path
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            if len(values) >= 4:
                return str(values[3])
        return ""

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Index")
        if not folder:
            return
        folder = normalize_path(folder)
        if not os.path.isdir(folder):
            messagebox.showerror(APP_TITLE, "Folder does not exist.")
            return
        if not self.indexer.add_target(folder):
            messagebox.showwarning(APP_TITLE, "Folder could not be indexed. It may already be indexed or overlap an existing target.")
            return
        self.reload_index()
        self.search_var.set(folder)

    def update_index(self):
        if not self.indexer.update():
            messagebox.showwarning(APP_TITLE, "Index update failed.")
            return
        self.reload_index()

    def open_selected(self):
        path = self._selected_path()
        if not path:
            return
        try:
            os.startfile(path)
        except Exception as error:
            messagebox.showerror(APP_TITLE, str(error))

    def show_selected(self):
        path = self._selected_path()
        if not path:
            return
        try:
            if os.path.isfile(path):
                subprocess.Popen(["explorer.exe", "/select,", path])
            else:
                os.startfile(path)
        except Exception as error:
            messagebox.showerror(APP_TITLE, str(error))

    def copy_selected_path(self):
        path = self._selected_path()
        if not path:
            return
        self.clipboard_clear()
        self.clipboard_append(path)
        self.set_status("Path copied to clipboard.")

    def clone_structure_prompt(self):
        src = filedialog.askdirectory(title="Select source folder")
        if not src:
            return
        dst = filedialog.askdirectory(title="Select destination folder")
        if not dst:
            return
        self.clone_src.delete(0, tk.END)
        self.clone_src.insert(0, src)
        self.clone_dst.delete(0, tk.END)
        self.clone_dst.insert(0, dst)
        self.clone_structure()

    def clone_structure(self):
        src = normalize_path(self.clone_src.get().strip())
        dst = normalize_path(self.clone_dst.get().strip())
        if not src or not dst or not os.path.isdir(src):
            messagebox.showerror(APP_TITLE, "Please provide valid source and destination folders.")
            return
        try:
            for current_path, _, _ in os.walk(src):
                relative = os.path.relpath(current_path, src)
                target = dst if relative == "." else os.path.join(dst, relative)
                os.makedirs(target, exist_ok=True)
            self.set_status("Folder structure cloned.")
            messagebox.showinfo(APP_TITLE, "Folder structure cloned.")
        except Exception as error:
            messagebox.showerror(APP_TITLE, str(error))

    def segregate_prompt(self):
        src = filedialog.askdirectory(title="Select source folder")
        if not src:
            return
        dst = filedialog.askdirectory(title="Select destination folder")
        if not dst:
            return
        self.seg_src.delete(0, tk.END)
        self.seg_src.insert(0, src)
        self.seg_dst.delete(0, tk.END)
        self.seg_dst.insert(0, dst)
        self.segregate()

    def segregate(self):
        src = normalize_path(self.seg_src.get().strip())
        dst = normalize_path(self.seg_dst.get().strip() or self.seg_src.get().strip())
        mode = self.seg_mode.get().strip().lower()
        value = self.seg_value.get().strip()
        if not src or not os.path.isdir(src):
            messagebox.showerror(APP_TITLE, "Source folder does not exist.")
            return
        if not value:
            messagebox.showinfo(APP_TITLE, "Please provide a rule value.")
            return
        os.makedirs(dst, exist_ok=True)
        moved = 0
        try:
            for filename in os.listdir(src):
                source_path = os.path.join(src, filename)
                if not os.path.isfile(source_path):
                    continue
                move = False
                target_folder = dst
                if mode == "extension":
                    if filename.lower().endswith(value.lower()):
                        move = True
                        target_folder = os.path.join(dst, value.replace(".", "").upper() or "FILES")
                elif mode == "size":
                    threshold = float(value)
                    if os.path.getsize(source_path) / (1024 * 1024) >= threshold:
                        move = True
                        target_folder = os.path.join(dst, f"OVER_{threshold:g}MB")
                elif mode == "age":
                    threshold = float(value)
                    if (time.time() - os.path.getmtime(source_path)) / 86400 >= threshold:
                        move = True
                        target_folder = os.path.join(dst, f"OLDER_{threshold:g}_DAYS")
                if move:
                    os.makedirs(target_folder, exist_ok=True)
                    target = self._safe_destination(target_folder, filename)
                    shutil.move(source_path, target)
                    moved += 1
            self.reload_index()
            messagebox.showinfo(APP_TITLE, f"Moved {moved} file(s).")
        except Exception as error:
            messagebox.showerror(APP_TITLE, str(error))

    def _safe_destination(self, folder, filename):
        target = os.path.join(folder, filename)
        if not os.path.exists(target):
            return target
        base, ext = os.path.splitext(filename)
        index = 1
        while True:
            candidate = os.path.join(folder, f"{base}_{index}{ext}")
            if not os.path.exists(candidate):
                return candidate
            index += 1


def main() -> None:
    app = LauncherApp()
    app.mainloop()


if __name__ == "__main__":
    main()
