from sudoku import Sudoku
from tkinter import *
from copy import deepcopy
from time import time



root = Tk()
root.title('Sudoku')
root.geometry('378x413')
root.resizable(0, 0)



canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)



def draw_board():
    canvas.create_line(42, 0, 42, 378, width=2, fill='lightgray')
    canvas.create_line(84, 0, 84, 378, width=2, fill='lightgray')
    
    canvas.create_line(168, 0, 168, 378, width=2, fill='lightgray')
    canvas.create_line(210, 0, 210, 378, width=2, fill='lightgray')
    
    canvas.create_line(294, 0, 294, 378, width=2, fill='lightgray')
    canvas.create_line(336, 0, 336, 378, width=2, fill='lightgray')

    canvas.create_line(0, 42, 378, 42, width=2, fill='lightgray')
    canvas.create_line(0, 84, 378, 84, width=2, fill='lightgray')

    canvas.create_line(0, 168, 378, 168, width=2, fill='lightgray')
    canvas.create_line(0, 210, 378, 210, width=2, fill='lightgray')

    canvas.create_line(0, 294, 378, 294, width=2, fill='lightgray')
    canvas.create_line(0, 336, 378, 336, width=2, fill='lightgray')

    canvas.create_line(126, 0, 126, 378, width=4, fill='black')
    canvas.create_line(252, 0, 252, 378, width=4, fill='black')
    canvas.create_line(0, 126, 378, 126, width=4, fill='black')
    canvas.create_line(0, 252, 378, 252, width=4, fill='black')



puzzle_cells = []

def draw_nums():
    global x_pos, y_pos, puzzle, cell_values
    for y_cord, row in enumerate(puzzle):
        for x_cord, num in enumerate(row):
            x_pos = 20 + x_cord * 42
            y_pos = 20 + y_cord * 42
            cell = chr(ord('a') + x_cord) + str(y_cord + 1)
            if num is None:
                # Only draw numbers for empty cells
                cell_id = canvas.create_text(x_pos, y_pos, text="", fill='gray', font=('Arial', 35, 'bold'), tags=(f"text_{cell}"))
                puzzle_cells.append(cell_id)
            else:
                # Don't allow editing filled cells
                cell_id = canvas.create_text(x_pos, y_pos, text=str(num), fill='gray', font=('Arial', 35, 'bold'), tags=(f"text_{cell}", "uneditable"))
            cell_values[cell] = num


_puzzle = Sudoku(3, seed=time()).difficulty(0.6)
puzzle = deepcopy(_puzzle.board)
solution = deepcopy(_puzzle.solve().board)
x_pos = 20
y_pos = 20
cell_values = {}

def get_puzzle_initial_value(cell):
    col = ord(cell[0]) - ord('a')
    row = int(cell[1]) - 1
    return _puzzle.board[row][col]

def play_again():
    global _puzzle, puzzle, win_gui
    _puzzle = Sudoku(3, seed=time()).difficulty(0.6)
    puzzle = deepcopy(_puzzle.board)
    solution = deepcopy(_puzzle.solve())
    canvas.delete("all")
    draw_board()
    draw_nums()
    win_gui.destroy()
    root.update()

def draw_ans(event):
    global win_gui
    cell = detect_pos(event)
    num = get_puzzle_initial_value(cell)
    if num is None:
        global x_pos, y_pos, puzzle, cell_values, puzzle_cells
        if cell:
            cell_id = canvas.find_withtag(f"text_{cell}")
            # Only allow adding numbers to empty cells in the puzzle and not in puzzle_cells
            if cell_values[cell] is None and not cell_id in puzzle_cells:
                new_value = 1  # Start with 1 for empty cells
            else:
                if cell_id not in puzzle_cells:
                    new_value = (cell_values[cell] % 9) + 1
            update_cell(cell, new_value)

    if None not in [num for row in puzzle for num in row] and (solution == puzzle):
        win_gui = Tk()
        win_gui.title('You Won')
        win_gui.geometry('250x75')
        Label(win_gui, text='Congratulations! You Won.', font=('bold')).pack()
        Button(win_gui, text='Play Again', font=('bold'), bg='lightgray', command=play_again).pack(side=BOTTOM)

def delete_num(event):
    cell = detect_pos(event)
    cell_id = canvas.find_withtag(f"text_{cell}")
    initial_value = get_puzzle_initial_value(cell)
    if cell_id and cell_id not in puzzle_cells and initial_value is None:
        update_cell(cell, None)

def update_cell(cell, value):
    global x_pos, y_pos, puzzle, cell_values
    x_cord, y_cord = ord(cell[0]) - ord('a'), int(cell[1]) - 1
    puzzle[y_cord][x_cord] = value
    x_pos = 20 + x_cord * 42
    y_pos = 20 + y_cord * 42
    canvas.delete(f"text_{cell}")  # Delete the old text
    if value is not None:
        canvas.create_text(x_pos, y_pos, text=str(value), fill='blue', font=('Arial', 35, 'bold'), tags=f"text_{cell}")
    else:
        canvas.create_text(x_pos, y_pos, text="", fill='gray', font=('Arial', 35, 'bold'), tags=f"text_{cell}")

    cell_values[cell] = value

def detect_pos(event):
    x_cord, y_cord = event.x // 42, event.y // 42
    if 0 <= x_cord <= 8 and 0 <= y_cord <= 8:
        return chr(ord('a') + x_cord) + str(y_cord + 1)
    


canvas.bind("<Motion>", detect_pos)
canvas.bind("<Button-1>", draw_ans)
canvas.bind("<Button-3>", delete_num)

Button(root, text='Play Again', font=('bold'), bg='lightgray', width=12, height=1, command=play_again).pack(side=BOTTOM, pady=1)
Label(root, text='Youssef Elebiary', font=('bold', 10)).place(x=1, y=391)

draw_board()
draw_nums()

root.mainloop()