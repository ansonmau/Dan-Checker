from parser.headers import get_headers_by_source
from transaction.transaction import Transaction
from logger.logger import get_logger
from readers.CsvReader import CsvReader

logger = get_logger("Bank-Parsers")


def parse_rbc(cr: CsvReader, results: list):
    first_data_row = 1  # line 0 is headers
    headers        = get_headers_by_source("rbc")

    for i in range(first_data_row, cr.get_num_rows()):
        # get_value shorthand
        gv = lambda x, i=i: cr.get_value(row=i, col=x)

        # ───────────────────────────< value checking >───────────────────────────
        acc_type   = f"RBC-Bank-Transaction"
        date       = gv(headers["date"]) or "Unknown Date"
        location   = gv(headers["location"]) or "Unknown Location"
        # if usd, put that in the location so user knows
        if gv(headers["extras"]["amount_usd"]):
            location = " ".join([location, "(USD)"])
            amount = gv(headers["extras"]["amount_usd"])
        else:
            amount = gv(headers["extras"]["amount_cad"]) or 0

        # typecheck
        date = str(date)
        location = str(location)
        amount = float(amount)

        logger.debug(f"Values grabbed -> {acc_type} | {date} | {location} | {amount}")
        # ─────────────────────────< append to results >───────────────────────
        t = Transaction()
        t.set_account_type(acc_type)
        t.set_date(date, "rbc")
        t.set_location(location)
        t.set_amount(amount)
        results.append(t)

    return 0

def parse_td(cr: CsvReader, results: list):
    first_data_row = 0
    headers        = get_headers_by_source("td")

    for i in range(first_data_row, cr.get_num_rows()):
        #get_value shorthand
        gv = lambda x, i=i: cr.get_value(row=i, col=x)

        # ───────────────────────────< value checking >───────────────────────────
        acc_type   = f"TD-Bank-Transaction"
        date       = gv(headers["date"]) or "Unknown Date"
        location   = gv(headers["location"]) or "Unknown Location"
        amount_in  = gv(headers["extras"]["amount_in"]) or 0
        amount_out = gv(headers["extras"]["amount_out"]) or 0
        amount = float(amount_out) - float(amount_in)

        # typecheck
        location = str(location)

        logger.debug(f"Values grabbed -> {acc_type} | {date} | {location} | {amount_out} - {amount_in} = {amount}")
        # ─────────────────────────< append to results >───────────────────────
        t = Transaction()
        t.set_account_type(acc_type)
        t.set_date(date, "td")
        t.set_location(location)
        t.set_amount(amount)
        results.append(t)

    return 0
