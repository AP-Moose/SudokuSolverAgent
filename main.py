import tkinter as tk
from sudoku_gui import SudokuGUI

def main():
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
