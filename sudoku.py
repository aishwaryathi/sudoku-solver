#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def backtracking(board):
    if validate_sudoku(board):
        return board 

    nums_to_fill = [(key, value) for key, value in board.items() if value == 0]

    if not nums_to_fill:
        return None  # If there are no empty cells, and it's not solved, the board is unsolvable

    min_heur_dict = {}
    min_length = float('inf')

    for key, _ in nums_to_fill:
        constraint_values = get_min_heuristic(board, key)
        min_heur_dict[key] = constraint_values

        if len(constraint_values) < min_length:
            min_length = len(constraint_values)
            selected_key = key

    for value in min_heur_dict[selected_key]:
        new_board = board.copy()
        new_board[selected_key] = value
        result = backtracking(new_board)

        if result is not None:
            return result

    return None

def validate_sudoku(board):
    value = 0
    if value in board.values():
        return False
    else:
        return True
def get_min_heuristic(board, key):
    remove_num = [i for i in range(1, 10)]
    grid = get_grid(board, key)
    row = get_row(board, key)
    column = get_column(board, key)

    for value in grid.values():
        if value in remove_num:
            remove_num.remove(value)
    for value in row.values():
        if value in remove_num:
            remove_num.remove(value)
    for value in column.values():
        if value in remove_num:
            remove_num.remove(value)
    return remove_num

def get_column(board, position):
    col = position[1]
    column = {key: value for key, value in board.items() if key[1] == col}
    return column
def get_row(board, position):
    pos = position[0] 
    row_col = pos + position[1]
    row = {key: value for key, value in board.items() if key.startswith(pos)}
    return row

def get_grid(board, position):
    alpha_dict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9}
    row = alpha_dict.get(position[0])
    col = int(position[1])
    grid_start_row = 3 * ((row - 1) // 3) + 1
    grid_start_col = 3 * ((col - 1) // 3) + 1
    grid = {}
    for i in range(grid_start_row, grid_start_row + 3):
        for j in range(grid_start_col, grid_start_col + 3):
            cell_key = f"{list(alpha_dict.keys())[list(alpha_dict.values()).index(i)]}{j}"
            grid[cell_key] = board.get(cell_key, None)
    return grid

if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
