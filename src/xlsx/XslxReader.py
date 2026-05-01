import openpyxl 

class XlsxReader:                                                                                                                                                                  
  def __init__(self):                                                                                                                                                            
      self._file_path = None                                                                                                                                                     
      self._workbook = None                                                                                                                                                      
      self._sheet = None
                                                                                                                                                                                 
  def set_target_file(self, file_path: str):
      self._file_path = file_path                                                                                                                                                
      self._workbook = None
      self._sheet = None

  def open(self, sheet_name: str = ""):                                                                                                                                        
      if not self._file_path:
          raise ValueError("No target file set. Call set_target_file() first.")                                                                                                  
      self._workbook = openpyxl.load_workbook(self._file_path, read_only=True, data_only=True)
      self._sheet = self._workbook[sheet_name] if sheet_name else self._workbook.active                                                                                          
                                                                                                                                                                                 
  def get_value(self, row: int, col: int):                                                                                                                                       
      if self._sheet is None:                                                                                                                                                    
          raise RuntimeError("File not opened. Call open() first.")
      return self._sheet.cell(row=row, column=col).value
