# ──────────────────────────< external imports >──────────────────────────
import sys
from PyQt6.QtWidgets import QApplication

# ─────────────────────────────< my imports >─────────────────────────────
from ui.file_select.main_widget import MainWidget as FileSelect
from ui.window                  import DualItemListWindow
from parser.parser              import Parser
from util                       import get_root, save_transactions, load_transactions
from logger.logger              import get_logger, MyLogger
import init

TESTING = 0 # set to true to use main_test instead of main
ROOT = get_root()
logger = get_logger("Main")

# ──────────────────────────────────────────────────────────────────────
# ╭────────────────────────────────────────────────╮
# │                    Release                     │
# ╰────────────────────────────────────────────────╯
def main():
    # ────────────────────────────< logger setup >────────────────────────────
    date = 0
    log_file_name = f"{date}.log"
    MyLogger.add_file_handler(ROOT / "logs" / log_file_name)
    MyLogger.add_stream_handler()
    logger.debug("Log file setup successful")

    # ────────────────────────────────< init >────────────────────────────────
    err = init.full_init()
    if ( err ):
        raise ValueError("Init failed")
    logger.debug("Init successful")
        
    # ─────────────────────────< start file select >───────────────────────
    app = QApplication(sys.argv)
    window = FileSelect(run)
    window.show()
    sys.exit(app.exec())


def run(xlsx_path, csv_path, bank_type):
    qb_transactions     =   [] 
    bank_transactions   =   []

    parser = Parser()
    parser.parse_qb(xlsx_path, qb_transactions)
    parser.parse_bank_statement(csv_path, bank_type, bank_transactions)

    unmatched_bank_ts = []
    for i in range(len(bank_transactions)):
        if bank_transactions[i] in qb_transactions:
            qb_transactions.remove(bank_transactions[i])
        else:
            unmatched_bank_ts.append(bank_transactions[i])

    # save_transactions(ROOT / 'data' / 'qb.txt', qb_transactions)
    # save_transactions(ROOT / 'data' / 'bank.txt', unmatched_bank_ts)
                          
    win1 = DualItemListWindow(qb_transactions, unmatched_bank_ts, "Unmatched Transactions", "Quickbooks", "Bank")
    win1.show()

    return 0

# ──────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────
# ╭────────────────────────────────────────────────╮
# │                    Testing                     │
# ╰────────────────────────────────────────────────╯
def test1():
    qb = []
    bank = []

    load_transactions(ROOT / 'data' / 'qb.txt', qb)
    load_transactions(ROOT / 'data' / 'bank.txt', bank)

    win1 = DualItemListWindow(qb, bank, "Unmatched Transactions", "Quickbooks", "Bank")
    win1.show()

def main_test():
    app = QApplication(sys.argv)
    run("/home/ansonmau/dev/dan-checker/data/QB.xlsx", "/home/ansonmau/dev/dan-checker/data/bank.csv", "TD")
    sys.exit(app.exec())
# ──────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    if TESTING:
        test1()
    else:
        main()
