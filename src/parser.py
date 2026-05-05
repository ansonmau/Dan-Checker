from readers.CsvReader import CsvReader
from readers.XlsxReader import XlsxReader
from transaction.transaction import Transaction

TEMP_FAIL_VAL = 1

class Parser:
    def __init__(self):
        pass
    
    def parse_qb(self, xlsx_path:str, results:list):
        """
        params:
            xlsx_path:  path to qb xlsx export 
            results:    list of results to append to
        return:
            error flag
        """
        xr = XlsxReader()
        xr.set_target_file(xlsx_path)
        if (not(xr.open("Sheet1"))):
            return TEMP_FAIL_VAL

        # data starts on row 4
        for i in range(4, xr.get_num_rows()):
            if not xr.get_value(row=i, col=xr.header("Type")):
                # type will always have a value for a valid transaction
                continue
            t = Transaction()
            t.set_account_type(xr.get_value(row=i, col=xr.header("Type")))
            t.set_date(xr.get_value(row=i, col=xr.header("Date")))
            t.set_location(xr.get_value(row=i, col=xr.header("Name")))
            val = xr.get_value(row=i, col=xr.header("Amount"))
            t.set_amount(float(val) if val else 0)
            results.append(t)

        return 0
        

    def parse_bank_statement(self, csv_path:str, results:list):
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

        for i in range(2, cr.num_rows):
            t = Transaction()
            t.set_account_type(cr.get_value(row=i, col=cr.headers["Account Type"]))
            t.set_account_number(cr.get_value(row=i, col=cr.headers["Account Number"]))
            t.set_date(cr.get_value(row=i, col=cr.headers["Transaction Date"]))
            t.set_location(cr.get_value(row=i, col=cr.headers["Description 1"]))
            cad_amount      =   cr.get_value(row=i, col=cr.headers["CAD$"])
            usd_amount      =   cr.get_value(row=i, col=cr.headers["USD$"])
            total_amount    =   0
            if (cad_amount):
                total_amount += float(cad_amount) * (-1) # bank reports as negative
            if (usd_amount):
                total_amount += float(usd_amount) * (-1) # see above
            t.set_amount(total_amount)
            results.append(t)

        return 0

