import os
import csv
from datetime import datetime


class FileIndexer:
    """
    AX File Operations Co-pilot

    File.csv is the ONLY persistent source of truth.

    Structure:

        Path | Folder | F1 | F2 | F3 | ...

    Files:
        report.pdf

    Folders:
        *Documents

    Deleted entries:
        [DELETED_20260817_1530]_report.pdf
        [DELETED_20260817_1530]_*Documents

    The Path column always retains the real historical path.
    """

    DELETED_PREFIX = "[DELETED_"
    FOLDER_PREFIX = "*"

    def __init__(self, output_file="File.csv", row_limit=999999):
        self.script_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.output_file = os.path.join(
            self.script_dir,
            output_file
        )

        self.row_limit = row_limit

    # =========================================================
    # PUBLIC
    # =========================================================

    def add_target(self, target_path):
        """
        Add and immediately index a target directory.

        The target becomes the highest-level Path in File.csv.
        """

        target_path = self._normalise_path(target_path)

        if not os.path.isdir(target_path):
            print(
                f"[INDEXER] Invalid folder: {target_path}"
            )
            return False

        records = self._load_csv()

        if self._target_exists_or_overlaps(
            target_path,
            records
        ):
            print(
                f"[INDEXER] Target already indexed "
                f"or overlaps an existing target:\n"
                f"{target_path}"
            )
            return False

        print(
            f"[INDEXER] Indexing target:\n"
            f"{target_path}"
        )

        new_records = self._scan_tree(
            target_path
        )

        records.extend(new_records)

        records = self._deduplicate_records(
            records
        )

        self._write_csv(records)

        print(
            f"[INDEXER] Added {len(new_records)} directories."
        )

        return True

    def update(self):
        """
        Incrementally reconcile the existing CSV with
        the current filesystem.

        Existing directories:
            - files checked
            - folders checked
            - new files detected
            - new folders detected
            - deleted files marked
            - deleted folders marked

        New directories are automatically discovered.
        """

        print("[INDEXER] Updating File.csv...")

        records = self._load_csv()

        if not records:
            print(
                "[INDEXER] File.csv contains no indexed directories."
            )
            return False

        roots = self._find_roots(records)

        updated = self._reconcile(
            records,
            roots
        )

        updated = self._deduplicate_records(
            updated
        )

        self._write_csv(updated)

        print(
            f"[INDEXER] Update complete."
        )

        print(
            f"[INDEXER] Indexed directories: "
            f"{len(updated)}"
        )

        return True

    def scan(self, target_dirs):
        """
        Compatibility method for older code.
        """

        for target in target_dirs:
            self.add_target(target)

    # =========================================================
    # SCANNING
    # =========================================================

    def _scan_tree(self, target):
        records = []

        for current_path, dirnames, filenames in os.walk(
            target
        ):

            dirnames.sort(
                key=str.lower
            )

            filenames.sort(
                key=str.lower
            )

            records.append(
                {
                    "Path": self._normalise_path(
                        current_path
                    ),
                    "Folder": self._folder_name(
                        current_path
                    ),
                    "Items": self._build_items(
                        filenames,
                        dirnames
                    )
                }
            )

        return records

    def _build_items(
        self,
        filenames,
        dirnames
    ):
        """
        Files first.
        Folders last.
        """

        files = sorted(
            filenames,
            key=str.lower
        )

        folders = sorted(
            dirnames,
            key=str.lower
        )

        return (
            files +
            [
                self.FOLDER_PREFIX + folder
                for folder in folders
            ]
        )

    # =========================================================
    # RECONCILIATION
    # =========================================================

    def _reconcile(
        self,
        records,
        roots
    ):
        """
        Reconcile the complete indexed tree.

        Existing historical records are retained.
        """

        old_by_path = {
            self._normalise_path(
                record["Path"]
            ): record
            for record in records
        }

        current_paths = set()

        updated = []

        # -----------------------------------------------------
        # 1. Re-scan all directories which still exist.
        # -----------------------------------------------------

        for path, old_record in old_by_path.items():

            if os.path.isdir(path):

                current_paths.add(path)

                new_record = self._reconcile_directory(
                    path,
                    old_record
                )

                updated.append(
                    new_record
                )

        # -----------------------------------------------------
        # 2. Discover new directories.
        # -----------------------------------------------------

        discovered = {}

        for root in roots:

            if not os.path.isdir(root):
                continue

            for current_path, dirnames, filenames in os.walk(
                root
            ):

                path = self._normalise_path(
                    current_path
                )

                if path in current_paths:
                    continue

                if path in discovered:
                    continue

                dirnames.sort(
                    key=str.lower
                )

                filenames.sort(
                    key=str.lower
                )

                discovered[path] = {
                    "Path": path,
                    "Folder": self._folder_name(
                        current_path
                    ),
                    "Items": self._build_items(
                        filenames,
                        dirnames
                    )
                }

        updated.extend(
            discovered.values()
        )

        # -----------------------------------------------------
        # 3. Preserve deleted directory rows.
        # -----------------------------------------------------

        for path, old_record in old_by_path.items():

            if path not in current_paths:

                deleted_record = (
                    self._preserve_deleted_directory(
                        old_record
                    )
                )

                updated.append(
                    deleted_record
                )

        return updated

    def _reconcile_directory(
        self,
        path,
        old_record
    ):
        """
        Compare one existing directory against
        its previous CSV representation.
        """

        try:
            entries = os.listdir(path)

        except (PermissionError, OSError) as error:

            print(
                f"[INDEXER] Access denied: "
                f"{path} -> {error}"
            )

            return old_record

        current_files = []
        current_folders = []

        for entry in entries:

            full_path = os.path.join(
                path,
                entry
            )

            try:

                if os.path.isdir(full_path):
                    current_folders.append(entry)

                elif os.path.isfile(full_path):
                    current_files.append(entry)

            except OSError:
                continue

        current_files.sort(
            key=str.lower
        )

        current_folders.sort(
            key=str.lower
        )

        current_items = self._build_items(
            current_files,
            current_folders
        )

        old_items = old_record.get(
            "Items",
            []
        )

        deleted_items = self._find_deleted_items(
            old_items,
            current_items
        )

        final_items = (
            current_items +
            deleted_items
        )

        return {
            "Path": path,
            "Folder": self._folder_name(path),
            "Items": self._sort_items(
                final_items
            )
        }

    # =========================================================
    # DELETION
    # =========================================================

    def _find_deleted_items(
        self,
        old_items,
        current_items
    ):
        """
        Preserve previously deleted items.

        A live item missing from the current filesystem
        receives a D_DATE marker.

        Existing D_DATE entries remain untouched.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M"
        )

        current_set = set(
            current_items
        )

        deleted = []

        for old_item in old_items:

            # Already deleted.
            if old_item.startswith(
                self.DELETED_PREFIX
            ):
                deleted.append(
                    old_item
                )
                continue

            if old_item not in current_set:

                deleted.append(
                    self._make_deleted_marker(
                        old_item,
                        timestamp
                    )
                )

        return deleted

    def _make_deleted_marker(
        self,
        item,
        timestamp
    ):
        return (
            f"{self.DELETED_PREFIX}"
            f"{timestamp}]_"
            f"{item}"
        )

    def _preserve_deleted_directory(
        self,
        record
    ):
        """
        Preserve a directory which no longer exists.

        Its Path remains intact so its historical location
        can still be searched/opened/displayed.
        """

        folder = record.get(
            "Folder",
            ""
        )

        if not folder.startswith(
            self.DELETED_PREFIX
        ):
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M"
            )

            folder = (
                f"{self.DELETED_PREFIX}"
                f"{timestamp}_"
                f"{folder}"
            )

        preserved_items = []

        for item in record.get(
            "Items",
            []
        ):

            if item.startswith(
                self.DELETED_PREFIX
            ):
                preserved_items.append(
                    item
                )

            else:
                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M"
                )

                preserved_items.append(
                    self._make_deleted_marker(
                        item,
                        timestamp
                    )
                )

        return {
            "Path": record["Path"],
            "Folder": folder,
            "Items": preserved_items
        }

    # =========================================================
    # ROOTS
    # =========================================================

    def _find_roots(
        self,
        records
    ):
        """
        Infer top-level indexed targets from File.csv.

        Example:

            C:\\Data
            C:\\Data\\Projects
            C:\\Data\\Projects\\Python

        Root:

            C:\\Data
        """

        paths = sorted(
            {
                self._normalise_path(
                    record["Path"]
                )
                for record in records
            },
            key=len
        )

        roots = []

        for path in paths:

            if not any(
                self._is_subpath(
                    path,
                    root
                )
                for root in roots
            ):
                roots.append(
                    path
                )

        return roots

    # =========================================================
    # TARGET VALIDATION
    # =========================================================

    def _target_exists_or_overlaps(
        self,
        target,
        records
    ):
        target = self._normalise_path(
            target
        )

        roots = self._find_roots(
            records
        )

        for root in roots:

            if root == target:
                return True

            if self._is_subpath(
                target,
                root
            ):
                return True

            if self._is_subpath(
                root,
                target
            ):
                return True

        return False

    # =========================================================
    # CSV LOAD
    # =========================================================

    def _load_csv(self):
        records = []

        current_file = self.output_file

        visited = set()

        while current_file:

            current_file = os.path.abspath(
                current_file
            )

            if current_file in visited:
                print(
                    "[INDEXER] CSV chain loop detected."
                )
                break

            visited.add(
                current_file
            )

            if not os.path.exists(
                current_file
            ):
                break

            next_file = None

            try:

                with open(
                    current_file,
                    "r",
                    newline="",
                    encoding="utf-8",
                    errors="replace"
                ) as file:

                    reader = csv.reader(
                        file
                    )

                    next(
                        reader,
                        None
                    )

                    for row in reader:

                        if not row:
                            continue

                        if row[0] == "CHN":

                            if len(row) >= 2:

                                next_file = row[1]

                                if not os.path.isabs(
                                    next_file
                                ):
                                    next_file = os.path.join(
                                        self.script_dir,
                                        next_file
                                    )

                            continue

                        if len(row) < 2:
                            continue

                        records.append(
                            {
                                "Path": row[0],
                                "Folder": row[1],
                                "Items": [
                                    item
                                    for item in row[2:]
                                    if item
                                ]
                            }
                        )

            except Exception as error:

                print(
                    f"[INDEXER] CSV read error: "
                    f"{error}"
                )

                break

            current_file = next_file

        return records

    # =========================================================
    # CSV WRITE
    # =========================================================

    def _write_csv(
        self,
        records
    ):
        if not records:
            print(
                "[INDEXER] Nothing to write."
            )
            return

        records.sort(
            key=lambda record: (
                len(record["Path"]),
                record["Path"].lower()
            )
        )

        max_items = max(
            len(record["Items"])
            for record in records
        )

        headers = (
            ["Path", "Folder"] +
            [
                f"F{i + 1}"
                for i in range(max_items)
            ]
        )

        self._remove_chain_files()

        file_number = 1
        row_count = 0

        current_file = self.output_file

        handle = open(
            current_file,
            "w",
            newline="",
            encoding="utf-8"
        )

        writer = csv.writer(
            handle
        )

        writer.writerow(
            headers
        )

        try:

            for record in records:

                if row_count >= self.row_limit:

                    next_file = (
                        self._chain_filename(
                            file_number + 1
                        )
                    )

                    writer.writerow(
                        [
                            "CHN",
                            next_file
                        ]
                    )

                    handle.close()

                    file_number += 1
                    row_count = 0

                    current_file = (
                        self._chain_filename(
                            file_number
                        )
                    )

                    handle = open(
                        current_file,
                        "w",
                        newline="",
                        encoding="utf-8"
                    )

                    writer = csv.writer(
                        handle
                    )

                    writer.writerow(
                        headers
                    )

                row = [
                    record["Path"],
                    record["Folder"]
                ]

                row.extend(
                    record["Items"]
                )

                while len(row) < len(headers):
                    row.append("")

                writer.writerow(
                    row
                )

                row_count += 1

        finally:

            handle.close()

        print(
            f"[INDEXER] File.csv written: "
            f"{len(records)} directories."
        )

    def _chain_filename(
        self,
        number
    ):
        base, extension = os.path.splitext(
            self.output_file
        )

        return os.path.basename(
            f"{base}_{number}{extension}"
        )

    def _remove_chain_files(self):

        base, extension = os.path.splitext(
            self.output_file
        )

        number = 2

        while True:

            filename = (
                f"{base}_{number}{extension}"
            )

            if not os.path.exists(
                filename
            ):
                break

            try:
                os.remove(
                    filename
                )
            except OSError:
                pass

            number += 1

    # =========================================================
    # UTILITIES
    # =========================================================

    def _folder_name(
        self,
        path
    ):
        name = os.path.basename(
            os.path.normpath(path)
        )

        return name or path

    def _sort_items(
        self,
        items
    ):
        """
        Live files
        live folders
        deleted entries
        """

        live_files = []
        live_folders = []
        deleted = []

        for item in items:

            if item.startswith(
                self.DELETED_PREFIX
            ):
                deleted.append(
                    item
                )

            elif item.startswith(
                self.FOLDER_PREFIX
            ):
                live_folders.append(
                    item
                )

            else:
                live_files.append(
                    item
                )

        live_files.sort(
            key=str.lower
        )

        live_folders.sort(
            key=str.lower
        )

        deleted.sort(
            key=str.lower
        )

        return (
            live_files +
            live_folders +
            deleted
        )

    def _deduplicate_records(
        self,
        records
    ):
        unique = {}

        for record in records:

            path = self._normalise_path(
                record["Path"]
            )

            record["Path"] = path

            unique[path] = record

        return list(
            unique.values()
        )

    def _normalise_path(
        self,
        path
    ):
        return os.path.normcase(
            os.path.normpath(
                os.path.abspath(path)
            )
        )

    def _is_subpath(
        self,
        child,
        parent
    ):
        child = self._normalise_path(
            child
        )

        parent = self._normalise_path(
            parent
        )

        if child == parent:
            return True

        parent = (
            parent.rstrip(os.sep)
            + os.sep
        )

        return child.startswith(
            parent
        )


# =============================================================
# DIRECT EXECUTION
# =============================================================

if __name__ == "__main__":

    indexer = FileIndexer()

    print()
    print("AX FILE OPERATIONS CO-PILOT")
    print("============================")
    print("1. Add folder")
    print("2. Update")
    print("3. Exit")
    print()

    choice = input(
        "Select: "
    ).strip()

    if choice == "1":

        path = input(
            "Folder path: "
        ).strip().strip('"')

        indexer.add_target(
            path
        )

    elif choice == "2":

        indexer.update()
