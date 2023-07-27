import random
import numpy as np


# function to generate a random sudoku
def generate_sudoku():
    # initialize an empty 9x9 grid
    grid = [[0 for j in range(9)] for i in range(9)]
    
    # randomly shuffle the values in the grid
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(values)
    for i in range(9):
        for j in range(9):
            grid[i][j] = values[(3*(i%3) + i//3 + j) % 9]
    
    # fill in the grid using backtracking
    fill_grid(grid, 0, 0)
    
    # convert the grid to a numpy array
    initial_sudoku = np.array(grid)
    
    # randomly remove some numbers to create empty spaces
    num_removed = 10 # adjust this number to control the difficulty level
    for i in range(num_removed):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0
    
    return grid, initial_sudoku

def fill_grid(grid, row, col):
    # if we have filled all rows, return True to indicate success
    if row == 9:
        return True
    
    # if we have filled all columns in the current row, move to the next row
    if col == 9:
        return fill_grid(grid, row + 1, 0)
    
    # if the current cell is already filled, move to the next column
    if grid[row][col] != 0:
        return fill_grid(grid, row, col + 1)
    
    # try all possible values for the current cell
    for val in range(1, 10):
        # check if val is valid in the current row, column, and 3x3 subgrid
        if is_valid(grid, row, col, val):
            grid[row][col] = val
            # recursively fill in the rest of the grid
            if fill_grid(grid, row, col + 1):
                return True
            # if the recursive call fails, backtrack and try the next value
            grid[row][col] = 0
    
    # if none of the values work, return False to backtrack
    return False


def is_valid(grid, row, col, val):
    # check if val is valid in the current row
    if val in grid[row]:
        return False
    
    # check if val is valid in the current column
    if val in [grid[i][col] for i in range(9)]:
        return False
    
    # check if val is valid in the current 3x3 subgrid
    subgrid_row = (row // 3) * 3
    subgrid_col = (col // 3) * 3
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if grid[i][j] == val:
                return False
    
    # if val is valid in all three checks, return True
    return True


# function to check if the user's solution is correct
def check_solution(initial_sudoku, solution):
    solution_flat = [num for row in solution for num in row]
    for i in range(81):
        if solution[i] != initial_sudoku[i]:
            return False
    return True


# function to solve the sudoku using graph algorithm
def solve_sudoku(grid):
    graph = {}
    for i in range(9):
        for j in range(9):
            neighbors = set()
            for k in range(9):
                if k != j:
                    neighbors.add((i, k))
                if k != i:
                    neighbors.add((k, j))
            box_i = (i // 3) * 3
            box_j = (j // 3) * 3
            for x in range(box_i, box_i + 3):
                for y in range(box_j, box_j + 3):
                    if x != i and y != j:
                        neighbors.add((x, y))
            graph[(i, j)] = neighbors

    def dfs(node, grid):
        if node is None:
            return True
        i, j = node
        if grid[i][j] != 0:
            return dfs(get_next_node(node), grid)
        neighbors = graph[node]
        used = set()
        for neighbor in neighbors:
            ni, nj = neighbor
            used.add(grid[ni][nj])
        for k in range(1, 10):
            if k not in used:
                grid[i][j] = k
                if dfs(get_next_node(node), grid):
                    return True
        grid[i][j] = 0
        return False

    def get_next_node(node):
        i, j = node
        if j < 8:
            return (i, j + 1)
        else:
            if i == 8:
                return None
            else:
                return (i + 1, 0)

    dfs((0, 0), grid)
    return grid
    # Solve the Sudoku by iteratively reducing the possibilities for each empty cell
    while True:
        updated = False
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0 and len(possibilities[i][j]) == 1:
                    grid[i][j] = list(possibilities[i][j])[0]
                    possibilities[i][j].clear()
                    updated = True
                elif grid[i][j] == 0:
                    for val in possibilities[i][j].copy():
                        # Check if the value is the only possibility in its row, column, or box
                        unique = True
                        for k in range(9):
                            if k != j and val in possibilities[i][k]:
                                unique = False
                                break
                            if k != i and val in possibilities[k][j]:
                                unique = False
                                break
                        box_i = (i // 3) * 3
                        box_j = (j // 3) * 3
                        for x in range(box_i, box_i + 3):
                            for y in range(box_j, box_j + 3):
                                if x != i and y != j and val in possibilities[x][y]:
                                    unique = False
                                    break
                        if unique:
                            grid[i][j] = val
                            possibilities[i][j] = set()
                            updated = True
                            break
        if not updated:
            break

    return grid


# main program
while True:
    grid, initial_sudoku = generate_sudoku()
    print("Here is your random sudoku:")
    for row in grid:
        print(row)

    # ask user for choice
    choice = input("Enter 1 to solve it yourself, 2 to let the computer solve it, or any other key to exit: ")
    
    

    # user wants to solve the sudoku himself
    if choice == "1":
        solution = grid
        print("Please enter the empty cells in the sudoku grid:")
        for i in range(9):
            for j in range(9):
                if(grid[i][j]!=0):
                    continue
                else:
                    solution[i][j]=int(input("Enter the empty cell at row {} and column {}: ".format(i+1, j+1)))
        print(solution)
    
        # code to check if the user's solution is correct
        pass


        # check if the user's solution is correct
        if check_solution(initial_sudoku, solution):
            print("Congratulations, you solved the sudoku!")
            choice2 = input("Enter 1 to solve another, or any other key to exit: ")
            if choice2 != "1":
                break
        else:
            print("Sorry, your solution is incorrect.")
            choice2 = input("Enter 1 to retry, or 2 to let the computer solve it: ")

            # user wants to retry
            if choice2 == "1":
                continue

            # user wants the computer to solve it
            else:
                # solve the sudoku using graph algorithm
                solution = solve_sudoku(grid)

                print("Here is the solution:")
                for row in solution:
                    print(row)

                choice2 = input("Enter 1 to solve another, or any other key to exit: ")
                if choice2 != "1":
                    break

    # user wants the computer to solve the sudoku
    elif choice == "2":
        # solve the sudoku using modified solve_sudoku function
        solution = solve_sudoku(grid)

        print("Here is the solution:")
        for row in solution:
            print(row)

        choice2 = input("Enter 1 to solve another, or any other key to exit: ")
        if choice2 != "1":
            break

    # user wants to exit
    else:
        break
