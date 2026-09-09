import LXComm

def run(row_data, lock_type="MAIN"):
    print(f"  [Neuron_1] Processing row data: {row_data}")
    
    if lock_type == "MAIN":
        LXComm.MAIN_LOCK = True
        print("  [Neuron_1] MAIN_LOCK acquired (True)")
        # Simulated sequential work
        print("  [Neuron_1] Work completed")
        LXComm.MAIN_LOCK = False
        print("  [Neuron_1] MAIN_LOCK released (False)")
        
    elif lock_type == "MODULE_1":
        LXComm.MODULE_1_LOCK = True
        print("  [Neuron_1] MODULE_1_LOCK acquired (True)")
        # Simulated sequential work
        print("  [Neuron_1] Work completed")
        LXComm.MODULE_1_LOCK = False
        print("  [Neuron_1] MODULE_1_LOCK released (False)")