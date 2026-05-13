import sys
from PyQt6.QtWidgets import QApplication

from ui.file_select import App 
from ui.window import DualItemListWindow
from parser import Parser
import init

from util import get_root, save_transactions, load_transactions

ROOT = get_root()
TESTING = 0


#                                   ╭────────────────────────────────────────────────╮
#                                   │                    Release                     │
#                                   ╰────────────────────────────────────────────────╯

def run(xlsx_path, csv_path):
    qb_transactions     =   [] 
    bank_transactions   =   []

    # print("ROOT: ", ROOT)

    parser = Parser()
    parser.parse_qb(xlsx_path, qb_transactions)
    parser.parse_bank_statement(csv_path, bank_transactions)

    unmatched_bank_ts   =   []
    for i in range(len(bank_transactions)):
        if bank_transactions[i] in qb_transactions:
            qb_transactions.remove(bank_transactions[i])
        else:
            unmatched_bank_ts.append(bank_transactions[i])

    save_transactions(ROOT / 'data' / 'qb.txt', qb_transactions)
    save_transactions(ROOT / 'data' / 'bank.txt', unmatched_bank_ts)
                          
    win1 = DualItemListWindow(qb_transactions, unmatched_bank_ts, "Unmatched Transactions", "Quickbooks", "Bank")
    win1.show()

    return 0


def main():
    err = init.full_init()
    if ( err ):
        raise ValueError("Init failed")
        
    app = QApplication(sys.argv)
    window = App(run)
    window.show()
    sys.exit(app.exec())

#                                   ╭────────────────────────────────────────────────╮
#                                   │                    Testing                     │
#                                   ╰────────────────────────────────────────────────╯

def test1():
    qb = []
    bank = []

    load_transactions(ROOT / 'data' / 'qb.txt', qb)
    load_transactions(ROOT / 'data' / 'bank.txt', bank)

    win1 = DualItemListWindow(qb, bank, "Unmatched Transactions", "Quickbooks", "Bank")
    win1.show()

def main_test():
    app = QApplication(sys.argv)
    run("/home/ansonmau/dev/dan-checker/data/QB.xlsx", "/home/ansonmau/dev/dan-checker/data/bank.csv")
    sys.exit(app.exec())



# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if TESTING:
        test1()
    else:
        main()
