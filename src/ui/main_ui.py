import tkinter as tk
from tkinter import filedialog


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Dan Checker")
        self.root.geometry("400x200")

        self.xlsx_path = tk.StringVar()
        self.csv_path = tk.StringVar()

        # xlsx row
        tk.Label(root, text="XLSX File:").grid(row=0, column=0, padx=10, pady=15, sticky="w")
        tk.Entry(root, textvariable=self.xlsx_path, width=35).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.browse_xlsx).grid(row=0, column=2, padx=5)

        # csv row
        tk.Label(root, text="CSV File:").grid(row=1, column=0, padx=10, pady=15, sticky="w")
        tk.Entry(root, textvariable=self.csv_path, width=35).grid(row=1, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.browse_csv).grid(row=1, column=2, padx=5)

        # run button
        tk.Button(root, text="Run", width=20, command=self.run).grid(row=2, column=0, columnspan=3, pady=20)

    def browse_xlsx(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if path:
            self.xlsx_path.set(path)

    def browse_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.csv_path.set(path)

    def run(self):
        pass
