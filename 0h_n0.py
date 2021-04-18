from z3 import *
import cProfile


def row_sum(i, j, X, dimension):
    # Returns the total number of blue cells seen row-wise by the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    return Sum(sum_left(i, j, X, dimension), sum_right(i, j, X, dimension))


def sum_left(i, j, X, dimension):
    # Returns the total number of blue cells seen to the left of the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    count = Sum(0, 0)
    isBlocked = False
    for c in range(j-1, -1, -1):
        count = If(isBlocked, count, If(X[i][c] > 0, count+1, count))
        isBlocked = Or(isBlocked, X[i][c] == RED)
    return count


def sum_right(i, j, X, dimension):
    # Returns the total number of blue cells seen to the right of the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    count = Sum(0, 0)
    isBlocked = False
    for c in range(j+1, dimension):
        count = If(isBlocked, count, If(X[i][c] > 0, count + 1, count))
        isBlocked = Or(isBlocked, X[i][c] == RED)
    return count


def col_sum(i, j, X, dimension):
    # Returns the total number of blue cells seen column-wise by the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    return Sum(sum_top(i, j, X, dimension), sum_bottom(i, j, X, dimension))


def sum_top(i, j, X, dimension):
    # Returns the total number of blue cells seen above the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    count = Sum(0, 0)
    isBlocked = False
    for r in range(i-1, -1, -1):
        count = If(isBlocked, count, If(X[r][j] > 0, count + 1, count))
        isBlocked = Or(isBlocked, X[r][j] == RED)
    return count


def sum_bottom(i, j, X, dimension):
    # Returns the total number of blue cells seen below the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    count = Sum(0, 0)
    isBlocked = False
    for r in range(i+1, dimension):
        count = If(isBlocked, count, If(X[r][j] > 0, count + 1, count))
        isBlocked = Or(isBlocked, X[r][j] == RED)
    return count


def count_blues(i, j, X, dimension):
    # Returns the total number of blue cells seen by the cell at the
    # given row, i, and column, j, of the game board
    # i : int
    #   The row of the queried cell.
    # j : int
    #   The column of the queried cell.
    # X : 2d array
    #   The given board state represented in SMT.
    # dimension : int
    #   The size of the board.
    return Sum(row_sum(i, j, X, dimension), col_sum(i, j, X, dimension))


####### Key #######
# Red = 0
RED = 0
# Empty = -1
# Blue = [1, dim] (number of other blue dots it can see)

# Blank instance of a 5x5 grid
# ((-1, -1, -1, -1, -1),
# (-1, -1, -1, -1, -1),
# (-1, -1, -1, -1, -1),
# (-1, -1, -1, -1, -1),
# (-1, -1, -1, -1, -1))

# Example instance of a 9x9 grid
# ((1, -1, -1, 4, -1, -1, -1, -1, 8),
# (-1, -1, 0, 4, -1, -1, -1, 3, 7),
# (5, -1, -1, -1, -1, -1, -1, -1, -1),
# (-1, -1, -1, 7, 7, -1, -1, -1, 6),
# (-1, 5, -1, -1, -1, -1, -1, -1, -1),
# (-1, 0, -1, 3, -1, 4, -1, -1, 9),
# (-1, -1, -1, 7, -1, -1, 8, 6, -1),
# (-1, 6, -1, -1, 6, -1, 7, 5, -1),
# (4, -1, 0, -1, -1, -1, -1, -1, 2))


def solve(instance):
    # Finds a solution to the given instance of 0hn0 if a solution exists.
    # instance : 2d array
    #   The given board state of an 0hn0 game, represented using our key.
    dimension = len(instance)

    X = [[Int("x_%s_%s" % (i+1, j+1)) for j in range(dimension)]
         for i in range(dimension)]  # x_1_1

    # Each cell contains a value in {0, ..., dim}
    # All cells must have a red or blue dot (none can be empty)
    cells_c = [And(RED <= X[i][j], X[i][j] <= dimension)
               for i in range(dimension) for j in range(dimension)]

    # All blue cells must see at least one other blue cell
    blue_1 = [Or(X[i][j] == RED,
                 count_blues(i, j, X, dimension) >= 1)
              for i in range(dimension) for j in range(dimension)]

    # All blue cells must see exactly as many blue cells as its value
    blue_val = [Or(X[i][j] == RED,
                   count_blues(i, j, X, dimension) == X[i][j])
                for i in range(dimension) for j in range(dimension)]

    oh_no_constraint = cells_c + blue_1 + blue_val

    instance_c = [If(instance[i][j] == -1,
                     True,
                     X[i][j] == instance[i][j])
                  for i in range(dimension) for j in range(dimension)]

    s = Solver()
    s.add(oh_no_constraint + instance_c)
    if s.check() == sat:
        m = s.model()
        r = [[m.evaluate(X[i][j]) for j in range(dimension)]
             for i in range(dimension)]
        print_matrix(r)
    else:
        print("failed to solve")


def time_benchmarking():
    # Runs time benchmarking on solve().

    instance4 = ((3, -1, 0, -1),
                 (-1, 2, -1, 2),
                 (-1, -1, -1, 2),
                 (3, -1, -1, 3))

    instance5 = ((-1, -1, 3, 0, 0),
                 (-1, -1, 3, -1, 3),
                 (-1, 0, 0, -1, 3),
                 (-1, -1, -1, 3, -1),
                 (1, 0, 3, 3, -1))

    instance6 = ((-1, -1, 4, 0, -1, 3),
                 (0, -1, 4, -1, -1, -1),
                 (-1, -1, 4, -1, -1, 3),
                 (-1, 4, -1, -1, 0, 0),
                 (-1, -1, -1, -1, 0, -1),
                 (1, -1, 2, 1, -1, 0))

    instance7 = ((-1, -1, -1, 7, -1, -1, 1),
                 (-1, 0, -1, -1, -1, 1, -1),
                 (3, -1, 4, 5, 3, -1, -1),
                 (-1, 1, -1, 6, -1, -1, 6),
                 (-1, -1, -1, 0, -1, -1, -1),
                 (2, -1, 3, -1, -1, -1, 5),
                 (0, -1, -1, -1, -1, 7, 7))

    instance8 = ((6, -1, 7, -1, -1, 6, -1, -1),
                 (-1, 0, -1, -1, 0, -1, 0, -1),
                 (-1, -1, -1, 2, -1, -1, -1, 6),
                 (-1, -1, 2, -1, -1, -1, -1, -1),
                 (4, 6, -1, -1, -1, 2, -1, -1),
                 (5, -1, -1, -1, 1, -1, 6, -1),
                 (-1, -1, -1, 3, -1, 4, -1, 0),
                 (1, -1, -1, -1, -1, 3, -1, -1))

    instance9 = ((1, -1, -1, 4, -1, -1, -1, -1, 8),
                 (-1, -1, 0, 4, -1, -1, -1, 3, 7),
                 (5, -1, -1, -1, -1, -1, -1, -1, -1),
                 (-1, -1, -1, 7, 7, -1, -1, -1, 6),
                 (-1, 5, -1, -1, -1, -1, -1, -1, -1),
                 (-1, 0, -1, 3, -1, 4, -1, -1, 9),
                 (-1, -1, -1, 7, -1, -1, 8, 6, -1),
                 (-1, 6, -1, -1, 6, -1, 7, 5, -1),
                 (4, -1, 0, -1, -1, -1, -1, -1, 2))

    cProfile.run("solve(" + str(instance4) + ")")
    cProfile.run("solve(" + str(instance5) + ")")
    cProfile.run("solve(" + str(instance6) + ")")
    cProfile.run("solve(" + str(instance7) + ")")
    cProfile.run("solve(" + str(instance8) + ")")
    cProfile.run("solve(" + str(instance9) + ")")

time_benchmarking()