import soto
import LXComm
import CONFIG
import SmallM1
import Neuron_1

def run(row_data):
    # Acquire external MainLOCK to hold orchestrator
    LXComm.MAIN_LOCK = True
    print(f"[Module_1] MAIN_LOCK acquired (True) for Main Row {LXComm.ROW_NO}: {row_data}")

    # Read child CSV
    print(f"[Module_1] Loading CSV: {CONFIG.MODULE_1_CSV_PATH}")
    params, rows = soto.read_csv_all(CONFIG.MODULE_1_CSV_PATH)

    for idx, r_data in enumerate(rows):
        frame = r_data.get("SubFrame")
        print(f"[Module_1] Processing SubRow {idx} | Frame: {frame}")

        target_module = LXComm.SUBTYPE_PIMD.get(frame)

        if target_module == "SmallM1":
            SmallM1.run(r_data)
        elif target_module == "Neuron_1":
            Neuron_1.run(r_data, lock_type="MODULE_1")
            
            # Module_1 wait check for internal lock
            while LXComm.MODULE_1_LOCK:
                pass

    # Release external MainLOCK to resume orchestrator
    LXComm.MAIN_LOCK = False
    print(f"[Module_1] MAIN_LOCK released (False) for Main Row {LXComm.ROW_NO}")