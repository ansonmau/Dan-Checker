from util import get_root

ROOT = get_root()

REQ_FOLDERS = [
        ROOT / 'data',
        ROOT / 'logs',
        ]

def init_folders():
    for f in REQ_FOLDERS:
        f.mkdir(exist_ok=True)

    return 0

def full_init():
    # ─< runs all init functions >──────────────────────────────────────────
    init_folders()
    return 0

