from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy, QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QGridLayout,
    QHBoxLayout,
)
from ui.file_select.upload_widget    import FileUploadWidget
from ui.file_select.bank_type_widget import MainWidget as BankTypeWidget

from logger.logger import get_logger

logger = get_logger("File-Select-Widget")


class MainWidget(QWidget):
    def __init__(self, run_function):
        super().__init__()
        self._bank_type    = None
        self._run_function = run_function

        self.setWindowTitle("Dan Checker")
        self.setFixedSize(500, 230)

        layout = QGridLayout()
        self.setLayout(layout)

        self._qb_widget = FileUploadWidget("Quickbooks File")
        layout.addWidget(self._qb_widget, 0, 0, 1, 3)

        self._bank_widget = FileUploadWidget("Bank File")
        layout.addWidget(self._bank_widget, 1, 0, 1, 3)

        # bank type
        self._bank_type_widget = BankTypeWidget()
        self._bank_type_widget.selected_type_emitter.connect(self._set_bank_type)
        layout.addWidget(self._bank_type_widget, 2, 0, 1, 3)

        # run button
        run_btn = QPushButton("DAN DAN DAN")
        run_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        run_btn.clicked.connect(self.run)
        layout.addWidget(run_btn, 3, 0, 1, 3)


    def run(self):
        conditions = [
                self._qb_widget.isSet(),
                self._bank_widget.isSet(),
                self._bank_type != None,
                ]

        if False in conditions:
            logger.debug(f"Conditions not met. Cannot start. -> {conditions}")
            return

        # self.run_function("/home/ansonmau/dev/dan-checker/data/QB.xlsx", "/home/ansonmau/dev/dan-checker/data/bank.csv")
        self._run_function(self._qb_widget.filePath(), self._bank_widget.filePath(), self._bank_type)

    def _set_bank_type(self, s: str):
        self._bank_type = s


