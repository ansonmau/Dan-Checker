# ╭────────────────────────────────────────────────╮
# │            Headers helper function             │
# ╰────────────────────────────────────────────────╯
def get_headers_by_source(source: str):
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
            "account_type":   0,
            "account_number": 1,
            "date":           2,
            "location":       4,
            "extras": {
                "amount_cad": 6,
                "amount_usd": 7,
                }
            })
    elif ( source == "td" ):
        # ─────────────────────────────────< TD >─────────────────────────────────
        headers.update({
            "date":     0,
            "location": 1,
            "extras": {
                "amount_out":  2,
                "amount_in":   3,
                "new_balance": 4,
                }
            })
    elif ( source=="qb" ):
        # ─────────────────────────────< Quickbooks >─────────────────────────────
        headers.update({
            "date":     8,
            "location": 12,
            "amount":   18,
            "extras": {
                "type": 6,
                "split": 16,
                "num": 10,
                "memo":        14,
                "new_balance": 20,
                },
            })

    return headers
         
