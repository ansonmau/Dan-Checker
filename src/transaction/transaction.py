from datetime import datetime
from transaction.location_parsing import parse_location

class Transaction:
    def __init__(self):
        self._account_type = None
        self._account_number = None
        self._date = None
        self._location = None
        self._amount = None

    def set_account_type(self, value: str):
        self._account_type = value

    def get_account_type(self) -> str:
        if self._account_type is None:
            raise ValueError("account_type has not been set.")
        return self._account_type

    def set_account_number(self, value: str):
        self._account_number = value

    def get_account_number(self) -> str:
        if self._account_number is None:
            raise ValueError("account_number has not been set.")
        return self._account_number

    def set_date(self, value):
        if not isinstance(value, datetime):
            # csv is formatted m/d/Y (no 0 padding)
            value = datetime.strptime(value, "%-m/%-d/%Y")
        self._date = value

    def get_date(self):
        if self._date is None:
            raise ValueError("date has not been set.")
        return datetime.strftime(self._date, "%m/%d/%Y")

    def set_location(self, value: str):
        self._location = parse_location(value)

    def get_location(self) -> str:
        if self._location is None:
            raise ValueError("location has not been set.")
        return self._location

    def set_amount(self, value: float):
        if not isinstance(value, float):
            raise TypeError("Passing non float value")
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

    def __eq__(self, other):
        c1 = self._date == other._date
        c2 = self._location == other._location
        c3 = self._amount == other._amount
        return c1 and c2 and c3

    def __hash__(self):
        s = f"{self._date!s}{self._location!s}{self._amount!s}"
        return hash(s)

    @property
    def save_inf(self):
        return {
                "account_type":   self._account_type,
                "account_number": self._account_number,
                "date":           self._date,
                "location":       self._location,
                "amount":         self._amount,
            }
