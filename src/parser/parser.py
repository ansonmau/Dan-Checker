from parser                  import bank_parsers
from readers.CsvReader       import CsvReader
from readers.XlsxReader      import XlsxReader
from transaction.transaction import Transaction
from logger.logger           import get_logger
from parser.bank_parsers     import parse_td, parse_rbc
from parser.headers          import get_headers_by_source


TEMP_FAIL_VAL = 1

logger = get_logger("Parser")

class Parser:
    def __init__(self):
        self._header_type = None
        self._headers = {}
        pass
    
    def parse_qb(self, xlsx_path:str, results:list):
        """
        params:
            xlsx_path:  path to qb xlsx export 
            results:    list of results to append to
        return:
            error flag
        """
        FIRST_DATA_ROW = 4

        xr = XlsxReader()
        xr.set_target_file(xlsx_path)
        err = xr.open("Sheet1")
        if (err):
            return TEMP_FAIL_VAL

        headers = get_headers_by_source("qb")
        for i in range(FIRST_DATA_ROW, xr.get_num_rows()):
            # shorthand get_value
            gv = lambda x, i=i: xr.get_value(row=i, col=x)

            if not gv(headers["extras"]["type"]):
                # empty type => not a transaction row
                continue
            
            # ───────────────────────────< value checking >───────────────────────────
            acc_type = "QB-Transaction"
            date     = gv(headers["date"]) or "Unknown Date"
            location = gv(headers["location"]) or "Unknown Location"
            val      = gv(headers["amount"]) or 0

            acc_type = str(acc_type)
            location = str(location)
            val      = float(val)

            logger.debug(f"Values grabbed -> {acc_type} | {date} | {location} | {val}")
            # ─────────────────────────< append to results >───────────────────────
            t = Transaction()
            t.set_account_type (acc_type)
            t.set_date         (date, 'qb')
            t.set_location     (location)
            t.set_amount       (val)
            results.append(t)

        return 0
        
    def parse_bank_statement(self, csv_path: str, bank_type: str, results: list):
        """
        params:
            csv_path:   path to qb export 
            results:    list of results to append to
        return:
            error flag
        """
        logger.debug(f"Bank type: {bank_type}")

        # ──────────────────────────< start csv reader >──────────────────────────
        cr = CsvReader()
        cr.set_target_file(csv_path)
        if (not(cr.open())):
            return TEMP_FAIL_VAL

        # ────────────────────────────< get results >──────────────────────────
        if bank_type == "td":
            parse_td(cr, results)
        elif bank_type == "rbc":
            parse_rbc(cr, results)

        return 0




