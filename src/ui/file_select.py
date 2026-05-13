from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QGridLayout
)


class App(QWidget):
    def __init__(self, run_function):
        super().__init__()
        self.run_function = run_function
        self.setWindowTitle("Dan Checker")
        self.setFixedSize(500, 130)

        layout = QGridLayout()
        self.setLayout(layout)

        # xlsx row
        layout.addWidget(QLabel("QB Exported file:"), 0, 0)
        self.xlsx_input = QLineEdit()
        layout.addWidget(self.xlsx_input, 0, 1)
        xlsx_browse = QPushButton("Browse")
        xlsx_browse.clicked.connect(self.browse_xlsx)
        layout.addWidget(xlsx_browse, 0, 2)

        # csv row
        layout.addWidget(QLabel("Bank statement: "), 1, 0)
        self.csv_input = QLineEdit()
        layout.addWidget(self.csv_input, 1, 1)
        csv_browse = QPushButton("Browse")
        csv_browse.clicked.connect(self.browse_csv)
        layout.addWidget(csv_browse, 1, 2)

        # run button
        run_btn = QPushButton("Compare")
        run_btn.clicked.connect(self.run)
        layout.addWidget(run_btn, 2, 0, 1, 3)

    def browse_xlsx(self):
        path, _ = QFileDialog.getOpenFileName(self, filter="Excel Files (*.xlsx)")
        if path:
            self.xlsx_input.setText(path)

    def browse_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, filter="CSV Files (*.csv)")
        if path:
            self.csv_input.setText(path)

    def run(self):
        # self.run_function("/home/ansonmau/dev/dan-checker/data/QB.xlsx", "/home/ansonmau/dev/dan-checker/data/bank.csv")
        self.run_function(self.xlsx_input.text(), self.csv_input.text())


