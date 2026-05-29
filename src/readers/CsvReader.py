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
        return 1

    def get_value(self, row: int, col: int):
        if not self._data:
            raise RuntimeError("File not opened. Call open() first.")

        return self._data[row][col]
    
    def get_objects(self, row_list:list[int], col_list:list[int]):
        if ( len(row_list) < 1 ) or ( len(col_list) < 1 ):
            return []

        all_obj = []
        for row_n in row_list:
            cur_obj = []
            for col_n in col_list:
                cur_obj.append(self.get_value(row_n, col_n))
            all_obj.append(cur_obj)
                
        return all_obj

    def get_num_rows(self):
        return len(self._data)

    def set_headers(self, headers):
        self._headers = headers
    
