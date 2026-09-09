# LXComm Configurable Multiplexer Architecture (v0 - Proof of Concept)

## 1. Overview & Problem Definition

When building data-driven automation systems driven by CSV matrices, repetitive logic frequently leaks across scripts. While parameter structures and row iteration techniques remain identical, hardcoding individual parsers and cross-script triggers bloats codebases and compounds testing friction.

This architecture decouples the execution engine using three distinct layers:

1. **Configurable Source of Truth (SOT)**: The CSV files defining parameters, frames, and payload data.
2. **Generic Extraction (`soto.py`)**: A centralized parser exposing standard row/parameter loading helpers.
3. **Variable & Routing Registry (`LXComm.py`)**: A shared communication layer acting as a **multiplexer switchboard** using Parameter-Module Dictionaries (`_PIMD`) and soft-locking flags.

---

## 2. Core Concepts & Taxonomy

| Term | Definition | Architectural Role |
| --- | --- | --- |
| **Configurable Source of Truth (SOT)** | The parent CSV matrix. | Houses runtime definitions, execution instructions, and variable data. |
| **Parameters** | The CSV column headers (e.g., `ID`, `Type`, `SubFrame`). | Define row schemas and select routing keys. |
| **Frames** | Specific symbolic values inside parameter columns (e.g., `F1`, `SubF2`). | Act as selector switches that map directly to functional modules. |
| **Variables** | Operational cell data (integers, floats, strings) attached to a row. | Passed to worker modules as execution payloads. |
| **`_PIMD`** | Parameter-Module Dictionary. | A key-value lookup table matching frames to their target module handles. |

---

## 3. Multiplexer Operational Model

The architecture functions as a hierarchical **time-division demultiplexer (Demux)** driven by tabular data:

```
[ main.csv (Source Stream) ]
            │
            ▼
     [ soto.py Parser ]
            │
            ▼
  [ Orchestrator (main.py) ]
            │
            ├──> Reads row data & updates LXComm.ROW_NO
            ├──> Evaluates frame symbol via LXComm.TYPE_PIMD
            │
     ┌──────┴───────────────────────────────────────┐
     │ Route F1                                     │ Route F2
     ▼                                              ▼
[ Module_1.py ]                                [ Neuron_1.py ]
     │                                              │
     ├── Sets LXComm.MAIN_LOCK = True               ├── Sets Lock Flag
     ├── Reads Module_1.csv (Sub-stream via soto)   ├── Executes sequential tasks
     ├── Demuxes SubFrames via SUBTYPE_PIMD         └── Clears Lock Flag
     │     ├── SubF1 ──> [ SmallM1.py ]
     │     └── SubF2 ──> [ Neuron_1.py ]
     │
     └── Sets LXComm.MAIN_LOCK = False
            │
            ▼
[ Orchestrator Unblocks -> Advances to Next Row ]

```

### Execution Flow:

1. **Stream Ingestion**: The orchestrator (`main.py`) invokes `soto.py` to parse the parent CSV into row records.
2. **Channel Selection**: For each record, the orchestrator inspects the designated parameter column (`Type`) and retrieves the bound module name from `LXComm.TYPE_PIMD`.
3. **Execution Gating**: If the target worker requires synchronous processing, it raises an execution lock (`MAIN_LOCK = True`). The orchestrator halts loop advancement.
4. **Nested Multiplexing (Sub-Layers)**: Worker modules (e.g., `Module_1.py`) can load localized sub-matrices (`Module_1.csv`) via `soto.py` and invoke nested `_PIMD` lookup trees, raising sub-locks (`MODULE_1_LOCK`) independently.
5. **Channel Release**: Upon task completion, the worker clears the lock flag, unblocking the parent loop to ingest the next row.

---

## 4. File Layout & Component Roles

```
.
├── CONFIG.py        # Centralized file paths and runtime constants
├── LXComm.py        # Shared state, lock flags, and PIMD routing tables
├── soto.py          # Pure CSV extraction utility methods
├── main.py          # Root orchestrator (main loop & frame demuxer)
├── Module_1.py      # Intermediate controller / nested matrix processor
├── Neuron_1.py      # Leaf worker with lock management
├── SmallM1.py       # Asynchronous / lock-free leaf worker
├── main.csv         # Top-level execution matrix
└── Module_1.csv     # Nested sub-execution matrix

```

### Module Responsibilities:

* **`CONFIG.py`**: Isolates physical file paths so testing environments can repoint data inputs without altering business logic.
* **`LXComm.py`**: Contains no computational logic. Serves strictly as a shared runtime cache for the active row index (`ROW_NO`), row payload (`CURRENT_ROW_DATA`), synchronization flags (`MAIN_LOCK`, `MODULE_1_LOCK`), and frame dispatch maps (`TYPE_PIMD`, `SUBTYPE_PIMD`).
* **`soto.py`**: Provides reusable, stateless CSV parsing functions (`read_csv_all`, `get_row_data`).
* **`main.py`**: Houses the primary iteration loop, registers current row metadata into `LXComm`, and routes row payloads to target handlers based on `_PIMD` matches.

---

## 5. Lock Management Protocol

To preserve execution order across modular scripts without multithreading overhead, synchronization uses lightweight state flags in `LXComm.py`:

* **`MAIN_LOCK` (Root Level)**: Raised by primary worker modules. Suspends the main orchestrator until entire multi-step or nested workflows conclude.
* **`MODULE_1_LOCK` (Sub-Level)**: Raised by child workers (such as `Neuron_1.py`) executing under a parent module. Suspends intermediate matrix iterations without blocking unrelated system components.
* **Lock-Free Operation**: Independent tasks (such as `SmallM1.py`) bypass lock toggling entirely, executing inline without blocking parent loops.

---

## 6. How to Extend the Pipeline

### Adding a New Frame Route:

1. Define your new module (e.g., `CustomWorker.py`) containing a `run(row_data)` entry point.
2. Open `LXComm.py` and register the new frame symbol under the appropriate dictionary:
```python
TYPE_PIMD = {
    "F1": "Module_1",
    "F2": "Neuron_1",
    "F3": "CustomWorker"  # New mapping
}

```


3. Add rows containing the `F3` symbol in `main.csv`. The orchestrator will dynamically route those rows to `CustomWorker.py` without requiring core logic modifications.