import tkinter as tk
from tkinter import messagebox
from sudoku_solver import solve, validate_sudoku

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")
        master.geometry("400x500")

        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        self.cells = {}
        for row in range(9):
            for col in range(9):
                cell = tk.Entry(self.master, width=2, font=('Arial', 18), justify='center')
                cell.grid(row=row, column=col, padx=1, pady=1)
                self.cells[(row, col)] = cell

    def create_buttons(self):
        solve_button = tk.Button(self.master, text="Solve", command=self.solve_sudoku)
        solve_button.grid(row=9, column=0, columnspan=3, pady=10)

        clear_button = tk.Button(self.master, text="Clear", command=self.clear_grid)
        clear_button.grid(row=9, column=3, columnspan=3, pady=10)

    def get_puzzle_string(self):
        return ''.join(self.cells[(row, col)].get() or '.' for row in range(9) for col in range(9))

    def set_puzzle_solution(self, solution):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, tk.END)
                self.cells[(row, col)].insert(0, solution[row * 9 + col])

    def solve_sudoku(self):
        puzzle = self.get_puzzle_string()
        if not validate_sudoku(puzzle):
            messagebox.showerror("Invalid Input", "Please enter a valid Sudoku puzzle.")
            return

        solution = solve(puzzle)
        if solution:
            self.set_puzzle_solution(''.join(solution[s] for s in solution))
        else:
            messagebox.showinfo("Unsolvable", "This Sudoku puzzle is unsolvable.")

    def clear_grid(self):
        for cell in self.cells.values():
            cell.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root)
    root.mainloop()
