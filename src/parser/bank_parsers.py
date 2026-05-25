from transaction.transaction import Transaction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from readers.CsvReader import CsvReader 

def _parse_rbc(cr: CsvReader, results: list):
    for i in range(2, cr.num_rows):
        acc_type     = "RBC Credit"
        acc_num      = cr.get_value(row=i, col=cr.headers["Account Number"])
        date         = cr.get_value(row=i, col=cr.headers["Transaction Date"])
        location     = cr.get_value(row=i, col=cr.headers["Description 1"])
        cad_amount   = cr.get_value(row=i, col=cr.headers["CAD$"])
        usd_amount   = cr.get_value(row=i, col=cr.headers["USD$"])

        total_amount = 0
        if (cad_amount):
            total_amount += float(cad_amount) * (-1) # bank reports as negative
        if (usd_amount):
            total_amount += float(usd_amount) * (-1) # see above

        t = Transaction()
        t.set_account_type(acc_type)
        t.set_account_number(acc_num)
        t.set_date(date)
        t.set_location(location)
        t.set_amount(total_amount)

        results.append(t)

    return 0

def _parse_td(cr: CsvReader, results: list):
    for i in range(2, cr.num_rows):
        acc_type     = "TD Credit"
        date         = cr.get_value(row=i, col=cr.headers["Transaction Date"])
        location     = cr.get_value(row=i, col=cr.headers["Description 1"])
        cad_amount   = cr.get_value(row=i, col=cr.headers["CAD$"])
        usd_amount   = cr.get_value(row=i, col=cr.headers["USD$"])

        total_amount = 0
        if (cad_amount):
            total_amount += float(cad_amount) * (-1) # bank reports as negative
        if (usd_amount):
            total_amount += float(usd_amount) * (-1) # see above

        t = Transaction()
        t.set_account_type(acc_type)
        t.set_account_number(acc_num)
        t.set_date(date)
        t.set_location(location)
        t.set_amount(total_amount)

        results.append(t)

    return 0
