class Transaction:                                                           
    def __init__(self):                                                                                                                                                            
      self._account_type = None                                                                                                                                                  
      self._account_number = None                                                                                                                                                
      self._date = None                                                                                                                                                          
      self._location = None
      self._amount = None
                                                                                                                                                                                 
# account_type
    def set_account_type(self, value: str):                                                                                                                                        
      self._account_type = value

    def get_account_type(self) -> str:
      if self._account_type is None:
          raise ValueError("account_type has not been set.")                                                                                                                     
      return self._account_type
                                                                                                                                                                                 
# account_number
    def set_account_number(self, value: str):
      self._account_number = value
                                                                                                                                                                                 
    def get_account_number(self) -> str:
      if self._account_number is None:                                                                                                                                           
          raise ValueError("account_number has not been set.")
      return self._account_number

# date
    def set_date(self, value):
      self._date = value                                                                                                                                                         

    def get_date(self):                                                                                                                                                            
      if self._date is None:
          raise ValueError("date has not been set.")
      return self._date

# location
    def set_location(self, value: str):
      self._location = value
                                                                                                                                                                                 
    def get_location(self) -> str:
      if self._location is None:                                                                                                                                                 
          raise ValueError("location has not been set.")
      return self._location

# amount
    def set_amount(self, value: float):
      self._amount = value
                                                                                                                                                                                 
    def get_amount(self) -> float:
      if self._amount is None:                                                                                                                                                   
          raise ValueError("amount has not been set.")
      return self._amount

    def __repr__(self):
      return (
          f"Transaction(account_type={self._account_type!r}, "
          f"account_number={self._account_number!r}, "                                                                                                                           
          f"date={self._date!r}, "
          f"location={self._location!r}, "                                                                                                                                       
          f"amount={self._amount!r})"
      )                    
