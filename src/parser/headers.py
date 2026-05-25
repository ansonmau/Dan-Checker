# ╭────────────────────────────────────────────────╮
# │            Headers helper function             │
# ╰────────────────────────────────────────────────╯
def headers(source: str):
    source = source.lower()
    srcs = ['rbc', 'td', 'qb']
    if ( source not in srcs ):
        raise ValueError("Tried to get headers for non-supported source `{}`".format(source))

    headers = {
            "account_type":   None,
            "account_number": None,
            "date":           None,
            "location":       None,
            "amount":         None,
            "extras":         {},
            }


    if ( source == "rbc" ):
        # ────────────────────────────────< RBC >──────────────────────────────
        headers.update({
            "account_type":   1,
            "account_number": 2,
            "date":           3,
            "location":       5,
            "extras": {
                "amount_cad": 7,
                "amount_usd": 8,
                }
            })
    elif ( source == "td" ):
        # ─────────────────────────────────< TD >─────────────────────────────────
        headers.update({
            "date":     1,
            "location": 2,
            "extras": {
                "amount_out":  3,
                "amount_in":   4,
                "new_balance": 5,
                }
            })
    elif ( source=="qb" ):
        # ─────────────────────────────< Quickbooks >─────────────────────────────
        headers.update({
            "date":     8,
            "location": 12,
            "amount":   18,
            "extras": {
                "type":        6,
                "split":       16,
                "num":         10,
                "memo":        14,
                "new_balance": 20,
                },
            })

    return headers
         
