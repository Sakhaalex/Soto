import csv
import os
from typing import List, Dict, Any, Optional

class SotoMatrix:
    """
    Universal Source of Truth Matrix Engine.
    Handles wide-column CSVs, parameter projections, and declarative queries.
    """
    def __init__(self, file_path: str, primary_key: Optional[str] = None):
        self.file_path = file_path
        self.primary_key = primary_key
        self.parameters: List[str] = []
        self.param_map: Dict[str, int] = {}
        self.rows: List[List[str]] = []
        self.pk_index: Dict[str, int] = {}
        
        if os.path.exists(file_path):
            self._load()

    def _load(self):
        with open(self.file_path, mode='r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            try:
                self.parameters = [h.strip() for h in next(reader)]
            except StopIteration:
                self.parameters = []
                return

            self.param_map = {param: idx for idx, param in enumerate(self.parameters)}
            pk_idx = self.param_map.get(self.primary_key) if self.primary_key else None

            for row_idx, row in enumerate(reader):
                self.rows.append(row)
                if pk_idx is not None and pk_idx < len(row):
                    val = row[pk_idx].strip()
                    if val:
                        self.pk_index[val] = row_idx

    def select(self, *required_params: str) -> List[Dict[str, str]]:
        """Projects only the requested subset of parameters from the wide CSV."""
        indices = {p: self.param_map[p] for p in required_params if p in self.param_map}
        results = []
        for row in self.rows:
            results.append({
                param: (row[idx].strip() if idx < len(row) else "")
                for param, idx in indices.items()
            })
        return results

    def filter(self, param: str, operator: str, value: Any) -> List[Dict[str, str]]:
        """Declarative filtering without writing lambdas (equals, contains, startswith, endswith)."""
        idx = self.param_map.get(param)
        if idx is None:
            return []

        target_val = str(value).lower().strip()
        matched = []

        for row in self.rows:
            cell_val = row[idx].strip().lower() if idx < len(row) else ""
            match = False
            
            if operator == "equals" and cell_val == target_val:
                match = True
            elif operator == "contains" and target_val in cell_val:
                match = True
            elif operator == "startswith" and cell_val.startswith(target_val):
                match = True
            elif operator == "endswith" and cell_val.endswith(target_val):
                match = True

            if match:
                matched.append({
                    p: (row[i].strip() if i < len(row) else "")
                    for p, i in self.param_map.items()
                })
        return matched

    def get_by_pk(self, pk_value: str) -> Optional[Dict[str, str]]:
        """O(1) lookup via Primary Key."""
        row_idx = self.pk_index.get(str(pk_value).strip())
        if row_idx is None:
            return None
        row = self.rows[row_idx]
        return {
            p: (row[i].strip() if i < len(row) else "")
            for p, i in self.param_map.items()
        }