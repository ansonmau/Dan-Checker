#!/usr/bin/env python
# ─────────────────────────────────────────────────────────────────────────────
#  main.py  –  entry point / smoke test
# ─────────────────────────────────────────────────────────────────────────────
import sys
from PyQt6.QtWidgets import QApplication
from ui.window import DualItemListWindow


class _Item:
    """Minimal mock object satisfying the card interface."""
    def __init__(self, date: str, location: str, amount: float):
        self._d, self._l, self._a = date, location, amount

    def get_date(self):     return self._d
    def get_location(self): return self._l
    def get_amount(self):   return self._a


def main():
    app = QApplication(sys.argv   # ── Sample data ───────────────────────────────────────────────────────────
    # Deliberately crafted so:
    #   • 2024-02-03 exists in both lists  (same location → yellow pop-out)
    #   • 2024-03-11 exists in both lists  (different locations → purple)
    #   • 2024-05-30 exists in both lists  (different locations → purple)

    left_items = [
        _Item("2024-01-15", "New York",    120.00),
        _Item("2024-02-03", "Los Angeles",  85.50),   # ← same date+location as right[0]
        _Item("2024-03-11", "Chicago",     200.00),   # ← same date, diff location
        _Item("2024-04-22", "Houston",      47.99),
        _Item("2024-05-30", "Phoenix",     310.00),   # ← same date, diff location
        _Item("2024-07-04", "Seattle",      99.00),
    ]

    right_items = [
        _Item("2024-02-03", "Los Angeles",  95.00),   # ← same date+location as left[1]
        _Item("2024-06-18", "San Diego",    60.00),
        _Item("2024-03-11", "Dallas",      175.50),   # ← same date, diff location
        _Item("2024-08-09", "Jacksonville", 88.00),
        _Item("2024-05-30", "Austin",      299.00),   # ← same date, diff location
        _Item("2024-10-21", "Denver",      145.00),
    ]

    win = DualItemListWindow(
        left_items,
        right_items,
        title       = "Unmatched Transactions",
        title_left  = "Bank Statement",
        title_right = "Expense Report",
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
