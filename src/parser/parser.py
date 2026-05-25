from readers.CsvReader import CsvReader
from readers.XlsxReader import XlsxReader
from transaction.transaction import Transaction
import parser.headers as header_module

TEMP_FAIL_VAL = 1

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

        headers = header_module.headers('qb')
        for i in range(FIRST_DATA_ROW, xr.get_num_rows()):
            gv = lambda x: xr.get_value(row=i, col=x)
            if not gv(headers["extras"]["type"]):
                # type will always have a value for a valid transaction
                continue
            
            # ───────────────────────────< value checking >───────────────────────────
            acc_type: str = str(gv(headers["account_type"])) or "Unknown"
            date     = gv(headers["date"]) or ""
            location = gv(headers["location"]) or ""
            val      = gv(headers["amount"]) or float(0)

            # ─────────────────────────< append to results >───────────────────────
            t = Transaction()
            t.set_account_type(acc_type)
            t.set_date(date)
            t.set_location(location)
            t.set_amount(val)
            results.append(t)

        return 0
        
    def parse_bank_statement(self, csv_path: str, results: list):
        """
        params:
            csv_path:   path to qb export 
            results:    list of results to append to
        return:
            error flag
        """
        cr = CsvReader()
        cr.set_target_file(csv_path)
        if (not(cr.open())):
            return TEMP_FAIL_VAL

        return 0




