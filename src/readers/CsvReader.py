import csv
class CsvReader:
    def __init__(self):
        self._file_path = None
        self._headers = {}
        self._data = []

    def set_target_file(self, file_path: str):
        self._file_path = file_path
        self._data = []

    def open(self):
        if not self._file_path:
            raise ValueError("No target file set. Call set_target_file() first.")
        with open(self._file_path, newline="", encoding="utf-8-sig") as f:
            self._data = list(csv.reader(f))
        self._get_headers()
        return 1

    def get_value(self, row: int, col: int):
        if not self._data:
            raise RuntimeError("File not opened. Call open() first.")
        return self._data[row][col]

    def _get_headers(self):
        if (not(self._data)):
            raise ValueError("data not yet set; call open() first")
        
        header_line = self._data[0]
        for col in range(len(header_line)):
            val = str(header_line[col]).strip()
            if (val == ""):
                continue 
            self._headers.update({val: col})

        return 1

    @property
    def num_rows(self):
        return len(self._data)
    
    @property
    def headers(self):
        return self._headers
