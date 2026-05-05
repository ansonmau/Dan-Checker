def parse_location(txt:str):
    if not txt:
        return "Unknown"

    location_patterns = {
            "Canada Computers": ["canada computers",],
            "Amazon": ["amazon", "amzn",],
            "New Egg": ["newegg", "new egg",],
            "Memory Express": ["memory express",],
            "Best Buy": ["best buy",],
            "Western Digital": ["western digital",],
    }

    txt = txt.lower() 
    for location in location_patterns:
        for p in location_patterns[location]:
            if p in txt:
                return location

    return txt
