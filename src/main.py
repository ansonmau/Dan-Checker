import tkinter as tk
from util import get_root
from ui.main_ui import App 

ROOT = get_root()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    return 0

if __name__ == "__main__":
    main()

