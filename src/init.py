from util import get_root

ROOT = get_root()

required_folders = [
        ROOT / 'data'
        ]

def init_folders():
    for f in required_folders:
        f.mkdir(exist_ok=True)

    return 0

def full_init():
# ├┤ runs all init functions ├─────────────────────────────────────────┤
    init_folders()
    return 0

