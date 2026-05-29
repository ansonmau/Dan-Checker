import sys
from pathlib import Path
from transaction.transaction import Transaction

# ────────────────────────────< root folder >──────────────────────────
def get_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent 


# ────────────────────< transaction saving / loading >────────────────────
def save_transactions(path: Path, save_list: list[Transaction]):
    with open(path, 'w') as f:
        for t in save_list:
            f.write(str(t.save_inf) + '\n')

def load_transactions(path: Path, output_list: list):
    with open(path, 'r') as f:
        for line in f.readlines():
            t = Transaction()
            # t._from_csv(line)
            output_list.append(t)
