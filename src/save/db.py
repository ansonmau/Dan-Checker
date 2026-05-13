import sqlite3

def main(root):
    conn = sqlite3.connect(root / 'data' / 'appdata.db')
    cursor = conn.cursor()

    
    conn.close()
    return 0

if __name__=="__main__":
    from pathlib import Path
    main(Path(__file__).resolve().parent.parent.parent)
