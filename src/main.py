import sys
from PyQt6.QtWidgets import QApplication
from ui.file_select import App 
from ui.window import DualItemListWindow
from parser import Parser
from util import get_root

ROOT = get_root()

def run(xlsx_path, csv_path):
    qb_transactions     =   [] 
    bank_transactions   =   []

    parser = Parser()
    parser.parse_qb(xlsx_path, qb_transactions)
    parser.parse_bank_statement(csv_path, bank_transactions)

    unmatched_bank_ts   =   []
    for i in range(len(bank_transactions)):
        if bank_transactions[i] in qb_transactions:
            qb_transactions.remove(bank_transactions[i])
        else:
            unmatched_bank_ts.append(bank_transactions[i])
                          

    # # comparison
    # qb_d = dict.fromkeys(qb_transactions)
    # for x in bank_transactions[:]:
    #     if x in qb_d:
    #         bank_transactions.remove(x)
    #         qb_transactions.remove(x)
    #         qb_d.pop(x)
    win1 = DualItemListWindow(unmatched_bank_ts, qb_transactions, "Unmatched Transactions", "Bank", "Quickbooks")
    win1.show()
            
    return 0



def main():
    app = QApplication(sys.argv)
    window = App(run)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

