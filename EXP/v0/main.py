import soto
import LXComm
import CONFIG
import Module_1
import Neuron_1

def main():
    params, rows = soto.read_csv_all(CONFIG.MAIN_CSV_PATH)
    print(f"[Orchestrator] Parameters loaded: {params}")

    for idx, row in enumerate(rows):
        # Update shared registry
        LXComm.ROW_NO = idx
        LXComm.CURRENT_ROW_DATA = row

        frame = row.get("Type")
        print(f"\n[Orchestrator] Row {idx} read | Frame: {frame} | Data: {row}")

        target_module = LXComm.TYPE_PIMD.get(frame)

        if target_module == "Module_1":
            Module_1.run(row)
        elif target_module == "Neuron_1":
            Neuron_1.run(row, lock_type="MAIN")
        else:
            print(f"[Orchestrator] No module registered for frame: {frame}")

        # Check external lock before proceeding to next row
        while LXComm.MAIN_LOCK:
            pass

    print("\n[Orchestrator] Completed all rows.")

if __name__ == "__main__":
    main()