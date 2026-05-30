from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QGridLayout,
    QHBoxLayout,
)

from logger.logger import get_logger

logger = get_logger("Bank-Type-Widget")

class MainWidget(QWidget):
    selected_type_emitter = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._lbl = QLabel("Bank Type:")
        self._btns = []

        self._btns.append(BankTypeButton("TD"))
        self._btns.append(BankTypeButton("RBC"))

        self._layout = QHBoxLayout(self)
        self._layout.addWidget(self._lbl)
        for b in self._btns:
            # ┌
            # │ - python uses reference so connect(lambda:     
            # │ self._select(b)) will not work                
            # │ - connect always passes a bool (is it          
            # │ checked) as first value so have to tank that   
            # └                                                 
            b.clicked.connect(lambda _, x=b: self._select(x))
            self._layout.addWidget(b)
        self._layout.addStretch() # push buttons to the left

    def _select(self, btn):
        self.selected_type_emitter.emit(btn._label.lower())
        logger.debug(f"Button selected. Emitting label: {btn._label}")
        for b in self._btns:
            if (btn == b):
                continue 
            b.setChecked(0)
        

class BankTypeButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self._label = label
        self.setCheckable(True)
        self.setFixedHeight(30)
        self.setFixedWidth(60)
        self._update()
        self.toggled.connect(self._update)

    def _update(self):
        if self.isChecked():
            self.setStyleSheet("""
                QPushButton {
                    border: 2px solid #2ecc71;
                    border-radius: 6px;
                    color: #2ecc71;
                    font-weight: bold;
                    background-color: #1a1a1a;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    border: 2px solid #555;
                    border-radius: 6px;
                    color: #777;
                    background-color: #1a1a1a;
                }
            """)

    def __eq__(self, other):
        return self._label == other._label

