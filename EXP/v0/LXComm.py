# Shared Variable Store and Registry

ROW_NO = 0
CURRENT_ROW_DATA = {}

# Locks
MAIN_LOCK = False
MODULE_1_LOCK = False

# Parameter Module Dictionaries (_PIMD)
# Format: { Parameter_Name: { Frame_Symbol: Module_Name } }
TYPE_PIMD = {
    "F1": "Module_1",
    "F2": "Neuron_1"
}

SUBTYPE_PIMD = {
    "SubF1": "SmallM1",
    "SubF2": "Neuron_1"
}