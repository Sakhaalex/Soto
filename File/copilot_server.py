import os
import json
import shutil
import socket
import subprocess
import threading
import webbrowser
import time

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from file_indexer import FileIndexer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_FILE = os.path.join(
    BASE_DIR,
    "file_copilot.html"
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "file_data.js"
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "File.csv"
)


class AXFileServer:
    """
    AX File Operations Co-pilot backend.

    Persistent state:
        File.csv

    Derived state:
        file_data.js

    File.csv is always treated as the authoritative
    representation of the indexed filesystem.
    """

    def __init__(self):
        self.indexer = FileIndexer(
            "File.csv"
        )

        self.lock = threading.RLock()

    # =========================================================
    # CSV / INDEX DATA
    # =========================================================

    def get_records(self):
        return self.indexer._load_csv()

    def generate_browser_data(self):
        """
        Convert File.csv records into a flat browser dataset.

        This file is only a cache/transport artifact.
        It is never treated as persistent state.
        """

        records = self.get_records()

        items = []

        for record in records:

            parent = record.get(
                "Path",
                ""
            )

            if not parent:
                continue

            for item in record.get(
                "Items",
                []
            ):

                if not item:
                    continue

                is_deleted = item.startswith(
                    self.indexer.DELETED_PREFIX
                )

                is_folder = (
                    item.startswith(
                        self.indexer.FOLDER_PREFIX
                    )
                    and not is_deleted
                )

                # -------------------------------------------------
                # Decode display name.
                # -------------------------------------------------

                if is_deleted:

                    name = self._deleted_display_name(
                        item
                    )

                elif is_folder:

                    name = item[1:]

                else:

                    name = item

                # -------------------------------------------------
                # Deleted entries must retain their historical
                # parent/path semantics.
                # -------------------------------------------------

                if is_deleted:

                    full_path = os.path.join(
                        parent,
                        name
                    )

                else:

                    full_path = os.path.join(
                        parent,
                        name
                    )

                extension = ""

                if is_folder:

                    extension = "folder"

                elif "." in name:

                    extension = (
                        "."
                        + name.rsplit(
                            ".",
                            1
                        )[1].lower()
                    )

                items.append(
                    {
                        "name": name,
                        "path": full_path,
                        "parent": parent,
                        "isFolder": is_folder,
                        "isDeleted": is_deleted,
                        "ext": extension
                    }
                )

        browser_data = (
            "window.sotoFileData = "
            + json.dumps(
                items,
                indent=2,
                ensure_ascii=False
            )
            + ";\nwindow.axFileData = window.sotoFileData;\n"
        )

        try:

            with open(
                DATA_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    browser_data
                )

        except OSError as error:

            print(
                "[SERVER] Could not generate file_data.js:",
                error
            )

        return items

    def _deleted_display_name(
        self,
        item
    ):
        """
        Convert deleted markers into the original item name.

        Supports both the current spec format:

            [DELETED_20260817_1530]_report.pdf

        and the older fallback format:

            D_20260817_1530_report.pdf
        """

        if item.startswith("[DELETED_"):

            closing = item.find("]_")

            if closing != -1:

                return item[closing + 2:]

        parts = item.split(
            "_",
            3
        )

        if len(parts) == 4:

            return parts[3]

        return item

    # =========================================================
    # TARGETS
    # =========================================================

    def get_targets(self):
        """
        Targets are inferred exclusively from File.csv.

        No separate target database is maintained.
        """

        records = self.get_records()

        if not records:
            return []

        paths = sorted(
            {
                self._normalise(
                    record["Path"]
                )
                for record in records
                if record.get("Path")
            },
            key=lambda value: (
                len(value),
                value.lower()
            )
        )

        targets = []

        for path in paths:

            if not any(
                self._is_subpath(
                    path,
                    root
                )
                for root in targets
            ):

                targets.append(
                    path
                )

        return targets

    # =========================================================
    # ADD FOLDER
    # =========================================================

    def add_folder(
        self,
        path
    ):
        path = self._normalise(
            path
        )

        if not os.path.isdir(path):

            return (
                False,
                "Folder does not exist."
            )

        with self.lock:

            result = self.indexer.add_target(
                path
            )

            if result:

                self.generate_browser_data()

                return (
                    True,
                    "Folder indexed successfully."
                )

            return (
                False,
                "Folder could not be indexed. "
                "It may already be indexed or overlap "
                "an existing target."
            )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        with self.lock:

            result = self.indexer.update()

            if result:

                self.generate_browser_data()

                return (
                    True,
                    "Index updated successfully."
                )

            return (
                False,
                "Index update failed."
            )

    # =========================================================
    # OPEN FILE
    # =========================================================

    def open_file(
        self,
        path
    ):

        if not path:

            return (
                False,
                "File path required."
            )

        path = self._normalise(
            path
        )

        if not os.path.isfile(path):

            return (
                False,
                "File does not exist."
            )

        try:

            os.startfile(
                path
            )

            return (
                True,
                "File opened."
            )

        except Exception as error:

            return (
                False,
                str(error)
            )

    # =========================================================
    # OPEN FOLDER
    # =========================================================

    def open_folder(
        self,
        path
    ):

        if not path:

            return (
                False,
                "Path required."
            )

        path = self._normalise(
            path
        )

        # -----------------------------------------------------
        # If the supplied path is a file, open Explorer with
        # that file selected.
        # -----------------------------------------------------

        if os.path.isfile(path):

            try:

                subprocess.Popen(
                    [
                        "explorer.exe",
                        "/select,",
                        path
                    ]
                )

                return (
                    True,
                    "File location opened."
                )

            except Exception as error:

                return (
                    False,
                    str(error)
                )

        # -----------------------------------------------------
        # Normal directory.
        # -----------------------------------------------------

        if os.path.isdir(path):

            try:

                os.startfile(
                    path
                )

                return (
                    True,
                    "Folder opened."
                )

            except Exception as error:

                return (
                    False,
                    str(error)
                )

        return (
            False,
            "Path does not exist."
        )

    # =========================================================
    # FOLDER STRUCTURE CLONING
    # =========================================================

    def recreate_structure(
        self,
        source,
        destination
    ):

        source = self._normalise(
            source
        )

        destination = self._normalise(
            destination
        )

        if not os.path.isdir(source):

            return (
                False,
                "Source folder does not exist."
            )

        if source == destination:

            return (
                False,
                "Source and destination cannot be identical."
            )

        try:

            for current_path, dirnames, _ in os.walk(
                source
            ):

                relative = os.path.relpath(
                    current_path,
                    source
                )

                if relative == ".":

                    target = destination

                else:

                    target = os.path.join(
                        destination,
                        relative
                    )

                os.makedirs(
                    target,
                    exist_ok=True
                )

            # The destination may itself be an indexed target.
            # Reconcile all known targets afterward.

            self.indexer.update()
            self.generate_browser_data()

            return (
                True,
                "Folder structure recreated."
            )

        except Exception as error:

            return (
                False,
                str(error)
            )

    # =========================================================
    # FILE SEGREGATION
    # =========================================================

    def segregate(
        self,
        source,
        mode,
        value=None,
        destination=None
    ):

        source = self._normalise(
            source
        )

        if not os.path.isdir(source):

            return (
                False,
                "Source folder does not exist."
            )

        if destination:

            destination = self._normalise(
                destination
            )

        else:

            destination = source

        mode = str(
            mode or ""
        ).strip().lower()

        try:

            moved = 0

            # -------------------------------------------------
            # Only files directly inside source are processed.
            # -------------------------------------------------

            for filename in os.listdir(
                source
            ):

                source_path = os.path.join(
                    source,
                    filename
                )

                if not os.path.isfile(
                    source_path
                ):

                    continue

                # =============================================
                # EXTENSION
                # =============================================

                if mode == "extension":

                    extension = os.path.splitext(
                        filename
                    )[1].lower()

                    if not extension:

                        folder_name = (
                            "NO_EXTENSION"
                        )

                    else:

                        folder_name = (
                            extension[1:]
                            .upper()
                        )

                    target_folder = os.path.join(
                        destination,
                        folder_name
                    )

                    os.makedirs(
                        target_folder,
                        exist_ok=True
                    )

                    target_path = (
                        self._safe_destination(
                            target_folder,
                            filename
                        )
                    )

                    shutil.move(
                        source_path,
                        target_path
                    )

                    moved += 1

                # =============================================
                # SIZE
                # =============================================

                elif mode == "size":

                    if value is None:

                        return (
                            False,
                            "Size value required."
                        )

                    try:

                        threshold = float(
                            value
                        )

                    except ValueError:

                        return (
                            False,
                            "Size value must be numeric."
                        )

                    size_mb = (
                        os.path.getsize(
                            source_path
                        )
                        / (
                            1024 * 1024
                        )
                    )

                    if size_mb < threshold:

                        continue

                    target_folder = os.path.join(
                        destination,
                        f"OVER_{threshold:g}MB"
                    )

                    os.makedirs(
                        target_folder,
                        exist_ok=True
                    )

                    target_path = (
                        self._safe_destination(
                            target_folder,
                            filename
                        )
                    )

                    shutil.move(
                        source_path,
                        target_path
                    )

                    moved += 1

                # =============================================
                # AGE
                # =============================================

                elif mode in (
                    "age",
                    "date"
                ):

                    if value is None:

                        return (
                            False,
                            "Age value required."
                        )

                    try:

                        threshold = float(
                            value
                        )

                    except ValueError:

                        return (
                            False,
                            "Age value must be numeric."
                        )

                    age_seconds = (
                        time.time()
                        - os.path.getmtime(
                            source_path
                        )
                    )

                    age_days = (
                        age_seconds
                        / 86400
                    )

                    if age_days < threshold:

                        continue

                    target_folder = os.path.join(
                        destination,
                        f"OLDER_{threshold:g}_DAYS"
                    )

                    os.makedirs(
                        target_folder,
                        exist_ok=True
                    )

                    target_path = (
                        self._safe_destination(
                            target_folder,
                            filename
                        )
                    )

                    shutil.move(
                        source_path,
                        target_path
                    )

                    moved += 1

                else:

                    return (
                        False,
                        f"Unknown segregation mode: {mode}"
                    )

            # -------------------------------------------------
            # Filesystem changed.
            # CSV must now be reconciled.
            # -------------------------------------------------

            self.indexer.update()
            self.generate_browser_data()

            return (
                True,
                f"{moved} file(s) moved."
            )

        except Exception as error:

            return (
                False,
                str(error)
            )

    # =========================================================
    # SAFE FILE MOVING
    # =========================================================

    def _safe_destination(
        self,
        folder,
        filename
    ):

        target = os.path.join(
            folder,
            filename
        )

        if not os.path.exists(
            target
        ):

            return target

        base, extension = os.path.splitext(
            filename
        )

        counter = 1

        while True:

            new_name = (
                f"{base}_{counter}"
                f"{extension}"
            )

            target = os.path.join(
                folder,
                new_name
            )

            if not os.path.exists(
                target
            ):

                return target

            counter += 1

    # =========================================================
    # FOLDER BROWSER
    # =========================================================

    def browse_folder(self):

        try:

            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            root.attributes(
                "-topmost",
                True
            )

            path = filedialog.askdirectory(
                title="Select Folder to Index"
            )

            root.destroy()

            return path or ""

        except Exception as error:

            print(
                "[SERVER] Folder browser error:",
                error
            )

            return ""

    # =========================================================
    # PATH UTILITIES
    # =========================================================

    def _normalise(
        self,
        path
    ):

        return os.path.normpath(
            os.path.abspath(
                os.path.expanduser(
                    str(path)
                )
            )
        )

    def _is_subpath(
        self,
        child,
        parent
    ):

        child = self._normalise(
            child
        )

        parent = self._normalise(
            parent
        )

        if child == parent:

            return True

        parent = (
            parent.rstrip(
                os.sep
            )
            + os.sep
        )

        return child.startswith(
            parent
        )


# =============================================================
# HTTP HANDLER
# =============================================================

class RequestHandler(
    BaseHTTPRequestHandler
):

    server_version = "AX-File-CoPilot/2.0"

    # =========================================================
    # RESPONSE HELPERS
    # =========================================================

    def _send_json(
        self,
        data,
        status=200
    ):

        payload = json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ).encode(
            "utf-8"
        )

        self.send_response(
            status
        )

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.send_header(
            "Content-Length",
            str(len(payload))
        )

        self.end_headers()

        self.wfile.write(
            payload
        )

    def _send_file(
        self,
        path,
        content_type
    ):

        if not os.path.isfile(
            path
        ):

            self.send_error(
                404,
                "File not found"
            )

            return

        try:

            with open(
                path,
                "rb"
            ) as file:

                data = file.read()

        except OSError as error:

            self.send_error(
                500,
                str(error)
            )

            return

        self.send_response(
            200
        )

        self.send_header(
            "Content-Type",
            content_type
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.send_header(
            "Content-Length",
            str(len(data))
        )

        self.end_headers()

        self.wfile.write(
            data
        )

    def _read_json(self):

        try:

            length = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

            if length <= 0:

                return {}

            raw = self.rfile.read(
                length
            )

            return json.loads(
                raw.decode(
                    "utf-8"
                )
            )

        except Exception:

            return {}

    def _api_error(
        self,
        message,
        status=400
    ):

        self._send_json(
            {
                "success": False,
                "error": message
            },
            status
        )

    # =========================================================
    # GET
    # =========================================================

    def do_GET(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path

        app = self.server.ax_app

        # -----------------------------------------------------
        # MAIN PAGE
        # -----------------------------------------------------

        if path == "/":

            self._send_file(
                HTML_FILE,
                "text/html; charset=utf-8"
            )

            return

        # -----------------------------------------------------
        # BROWSER DATA
        # -----------------------------------------------------

        if path == "/api/data":

            try:

                with app.lock:

                    data = (
                        app.generate_browser_data()
                    )

                    targets = (
                        app.get_targets()
                    )

                self._send_json(
                    {
                        "success": True,
                        "data": data,
                        "targets": targets
                    }
                )

            except Exception as error:

                self._send_json(
                    {
                        "success": False,
                        "error": str(error)
                    },
                    500
                )

            return

        # -----------------------------------------------------
        # TARGETS
        # -----------------------------------------------------

        if path == "/api/targets":

            self._send_json(
                {
                    "success": True,
                    "targets": app.get_targets()
                }
            )

            return

        # -----------------------------------------------------
        # FOLDER BROWSER
        # -----------------------------------------------------

        if path == "/api/browse-folder":

            selected = (
                app.browse_folder()
            )

            self._send_json(
                {
                    "success": bool(
                        selected
                    ),
                    "path": selected
                }
            )

            return

        # -----------------------------------------------------
        # GENERATED BROWSER DATA
        # -----------------------------------------------------

        if path == "/file_data.js":

            if not os.path.isfile(
                DATA_FILE
            ):

                app.generate_browser_data()

            self._send_file(
                DATA_FILE,
                "application/javascript; charset=utf-8"
            )

            return

        # -----------------------------------------------------
        # SERVER CONFIG
        # -----------------------------------------------------

        if path == "/server_config.js":

            payload = (
                "window.SOTO_SERVER_URL = '';\n"
                "window.AX_SERVER_ACTIVE = true;\n"
            ).encode(
                "utf-8"
            )

            self.send_response(
                200
            )

            self.send_header(
                "Content-Type",
                "application/javascript; charset=utf-8"
            )

            self.send_header(
                "Cache-Control",
                "no-store"
            )

            self.send_header(
                "Content-Length",
                str(len(payload))
            )

            self.end_headers()

            self.wfile.write(
                payload
            )

            return

        self.send_error(
            404,
            "Not found"
        )

    # =========================================================
    # POST
    # =========================================================

    def do_POST(self):

        parsed = urlparse(
            self.path
        )

        path = parsed.path

        body = self._read_json()

        app = self.server.ax_app

        # -----------------------------------------------------
        # ADD FOLDER
        # -----------------------------------------------------

        if path == "/api/add-folder":

            folder = body.get(
                "path"
            )

            if not folder:

                self._api_error(
                    "Folder path required."
                )

                return

            success, message = (
                app.add_folder(
                    folder
                )
            )

            self._send_json(
                {
                    "success": success,
                    "message": message,
                    "targets": app.get_targets()
                },
                200 if success else 400
            )

            return

        # -----------------------------------------------------
        # BROWSE + ADD FOLDER
        # -----------------------------------------------------

        if path == "/api/browse-folder":

            selected = app.browse_folder()

            if not selected:

                self._send_json(
                    {
                        "success": False,
                        "message": "Folder selection cancelled.",
                        "path": ""
                    },
                    200
                )

                return

            success, message = app.add_folder(
                selected
            )

            self._send_json(
                {
                    "success": success,
                    "message": message,
                    "path": selected,
                    "targets": app.get_targets()
                },
                200 if success else 400
            )

            return

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        if path == "/api/update":

            success, message = (
                app.update()
            )

            self._send_json(
                {
                    "success": success,
                    "message": message
                },
                200 if success else 500
            )

            return

        # -----------------------------------------------------
        # OPEN FILE
        # -----------------------------------------------------

        if path == "/api/open-file":

            success, message = (
                app.open_file(
                    body.get(
                        "path",
                        ""
                    )
                )
            )

            self._send_json(
                {
                    "success": success,
                    "message": message
                },
                200 if success else 400
            )

            return

        # -----------------------------------------------------
        # OPEN FOLDER
        # -----------------------------------------------------

        if path == "/api/open-folder":

            success, message = (
                app.open_folder(
                    body.get(
                        "path",
                        ""
                    )
                )
            )

            self._send_json(
                {
                    "success": success,
                    "message": message
                },
                200 if success else 400
            )

            return

        # -----------------------------------------------------
        # RECREATE STRUCTURE
        # -----------------------------------------------------

        if path == "/api/recreate-structure":

            source = body.get(
                "source",
                body.get(
                    "src_path",
                    ""
                )
            )

            destination = body.get(
                "destination",
                body.get(
                    "dest_path",
                    ""
                )
            )

            success, message = (
                app.recreate_structure(
                    source,
                    destination
                )
            )

            self._send_json(
                {
                    "success": success,
                    "message": message
                },
                200 if success else 400
            )

            return

        # -----------------------------------------------------
        # SEGREGATION
        # -----------------------------------------------------

        if path == "/api/segregate":

            source = body.get(
                "source",
                body.get(
                    "src_path",
                    ""
                )
            )

            destination = body.get(
                "destination",
                body.get(
                    "dest_path",
                    ""
                )
            )

            mode = body.get(
                "mode",
                body.get(
                    "rule_type",
                    ""
                )
            )

            value = body.get(
                "value",
                body.get(
                    "rule_value"
                )
            )

            success, message = (
                app.segregate(
                    source,
                    mode,
                    value,
                    destination
                )
            )

            self._send_json(
                {
                    "success": success,
                    "message": message
                },
                200 if success else 400
            )

            return

        # -----------------------------------------------------
        # LEGACY ACTION ROUTING
        #
        # This keeps compatibility with the current HTML while
        # allowing the server to use the cleaner endpoint API.
        # -----------------------------------------------------

        if path == "/api":

            action = body.get(
                "action",
                ""
            )

            # ---------------------------------------------
            # GET TARGETS
            # ---------------------------------------------

            if action == "get_targets":

                self._send_json(
                    {
                        "success": True,
                        "status": "success",
                        "targets": app.get_targets()
                    }
                )

                return

            # ---------------------------------------------
            # UPDATE
            # ---------------------------------------------

            if action == "update_index":

                success, message = (
                    app.update()
                )

                self._send_json(
                    {
                        "success": success,
                        "status": (
                            "success"
                            if success
                            else "error"
                        ),
                        "message": message,
                        "msg": message
                    }
                )

                return

            # ---------------------------------------------
            # OPEN FILE
            # ---------------------------------------------

            if action == "open_file":

                success, message = (
                    app.open_file(
                        body.get(
                            "path",
                            ""
                        )
                    )
                )

                self._send_json(
                    {
                        "success": success,
                        "status": (
                            "success"
                            if success
                            else "error"
                        ),
                        "message": message,
                        "msg": message
                    }
                )

                return

            # ---------------------------------------------
            # OPEN FOLDER
            # ---------------------------------------------

            if action == "open_folder":

                success, message = (
                    app.open_folder(
                        body.get(
                            "path",
                            ""
                        )
                    )
                )

                self._send_json(
                    {
                        "success": success,
                        "status": (
                            "success"
                            if success
                            else "error"
                        ),
                        "message": message,
                        "msg": message
                    }
                )

                return

            # ---------------------------------------------
            # RECREATE STRUCTURE
            # ---------------------------------------------

            if action == "recreate_structure":

                success, message = (
                    app.recreate_structure(
                        body.get(
                            "src_path",
                            ""
                        ),
                        body.get(
                            "dest_path",
                            ""
                        )
                    )
                )

                self._send_json(
                    {
                        "success": success,
                        "status": (
                            "success"
                            if success
                            else "error"
                        ),
                        "message": message,
                        "msg": message
                    }
                )

                return

            # ---------------------------------------------
            # ADVANCED SEGREGATION
            # ---------------------------------------------

            if action == "segregate_advanced":

                success, message = (
                    app.segregate(
                        body.get(
                            "src_path",
                            ""
                        ),
                        body.get(
                            "rule_type",
                            ""
                        ),
                        body.get(
                            "rule_value"
                        ),
                        body.get(
                            "dest_path"
                        )
                    )
                )

                self._send_json(
                    {
                        "success": success,
                        "status": (
                            "success"
                            if success
                            else "error"
                        ),
                        "message": message,
                        "msg": message
                    }
                )

                return

            # ---------------------------------------------
            # REMOVE TARGET
            #
            # Deliberately does not mutate File.csv.
            #
            # A target is not a separate database object.
            # Removing it from a UI list would otherwise
            # contradict the CSV-only architecture.
            # ---------------------------------------------

            if action == "remove_target":

                self._send_json(
                    {
                        "success": False,
                        "status": "error",
                        "message": (
                            "Targets are derived from File.csv "
                            "and cannot be removed independently."
                        ),
                        "msg": (
                            "Targets are derived from File.csv "
                            "and cannot be removed independently."
                        )
                    },
                    400
                )

                return

            self._send_json(
                {
                    "success": False,
                    "status": "error",
                    "message": (
                        f"Unknown API action: {action}"
                    ),
                    "msg": (
                        f"Unknown API action: {action}"
                    )
                },
                404
            )

            return

        self.send_error(
            404,
            "Not found"
        )

    # =========================================================
    # LOGGING
    # =========================================================

    def log_message(
        self,
        format,
        *args
    ):

        print(
            "[HTTP]",
            format % args
        )


# =============================================================
# SERVER STARTUP
# =============================================================

def find_free_port():

    socket_obj = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:

        socket_obj.bind(
            (
                "127.0.0.1",
                0
            )
        )

        return socket_obj.getsockname()[1]

    finally:

        socket_obj.close()


def start_server():

    app = AXFileServer()

    # ---------------------------------------------------------
    # Generate derived browser data if the persistent index
    # already exists.
    # ---------------------------------------------------------

    if os.path.isfile(
        CSV_FILE
    ):

        try:

            app.generate_browser_data()

        except Exception as error:

            print(
                "[SERVER] Initial data generation failed:",
                error
            )

    port = find_free_port()

    server = ThreadingHTTPServer(
        (
            "127.0.0.1",
            port
        ),
        RequestHandler
    )

    server.ax_app = app

    url = (
        f"http://127.0.0.1:{port}/"
    )

    print()
    print(
        "========================================"
    )
    print(
        "       AX FILE OPERATIONS CO-PILOT"
    )
    print(
        "========================================"
    )
    print()
    print(
        f"File index : {CSV_FILE}"
    )
    print(
        f"Server     : {url}"
    )
    print()
    print(
        "Persistent state : File.csv"
    )
    print(
        "Browser cache    : file_data.js"
    )
    print()
    print(
        "Press CTRL+C to stop the server."
    )
    print()

    threading.Timer(
        0.8,
        lambda: webbrowser.open(
            url
        )
    ).start()

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print()
        print(
            "[SERVER] Shutting down..."
        )

    finally:

        server.server_close()


if __name__ == "__main__":

    start_server()
