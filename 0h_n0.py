from z3 import *;

# DIMENSION is a constant representing the dimensions of the game grid
# e.g. DIMENSION = 9 corresponds to a 9x9 0h n0 grid
DIMENSION = 9

# returns the total number of blue cells seen row-wise by the cell at the
# given row, i, and column, j, of the game board
def row_sum(i, j):
    return Sum(sum_left(i, j), sum_right(i, j))

# returns the total number of blue cells seen to the left of the cell at the
# given row, i, and column, j, of the game board
def sum_left(i, j):
    count = Sum(0, 0)
    isBlocked = False
    for c in range (j-1, -1, -1):
      count = If(isBlocked, count, If(X[i][c] > 0, count+1, count))
      isBlocked = Or(isBlocked, X[i][c] == RED)
    return count

# returns the total number of blue cells seen to the right of the cell at the
# given row, i, and column, j, of the game board
def sum_right(i, j):
    count = Sum(0, 0)
    isBlocked = False
    for c in range (j+1, DIMENSION):
      count = If(isBlocked, count, If(X[i][c] > 0, count + 1, count))
      isBlocked = Or(isBlocked, X[i][c] == RED)
    return count

# returns the total number of blue cells seen column-wise by the cell at the
# given row, i, and column, j, of the game board
def col_sum(i, j):
    return Sum(sum_top(i, j), sum_bottom(i, j))

# returns the total number of blue cells seen above the cell at the
# given row, i, and column, j, of the game board
def sum_top(i, j):
    count = Sum(0, 0)
    isBlocked = False
    for r in range (i-1, -1, -1):
      count = If(isBlocked, count, If(X[r][j] > 0, count + 1, count))
      isBlocked = Or(isBlocked, X[r][j] == RED)
    return count

# returns the total number of blue cells seen below the cell at the
# given row, i, and column, j, of the game board
def sum_bottom(i, j):
    count = Sum(0, 0)
    isBlocked = False
    for r in range (i+1, DIMENSION):
      count = If(isBlocked, count, If(X[r][j] > 0, count + 1, count))
      isBlocked = Or(isBlocked, X[r][j] == RED)
    return count

# returns the total number of blue cells seen by the cell at the
# given row, i, and column, j, of the game board
def count_blues(i, j):
    return Sum(row_sum(i, j), col_sum(i, j))

####### Key #######
# Red = 0
RED = 0
# Empty = -1
# Blue = [1, dim] (number of other blue dots it can see)

X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(DIMENSION) ]
    for i in range(DIMENSION) ] # x_1_1

# each cell contains a value in {0, ..., dim}
# all cells must have a red or blue dot (none can be empty)
cells_c  = [ And(RED <= X[i][j], X[i][j] <= DIMENSION)
             for i in range(DIMENSION) for j in range(DIMENSION) ]


## All blue cells must see at least one other blue cell
blue_1 = [ Or(X[i][j] == RED,
              count_blues(i, j) >= 1)
              for i in range(DIMENSION) for j in range(DIMENSION) ]



## All blue cells must see exactly as many blue cells as its value
blue_val = [ Or(X[i][j] == RED,
              count_blues(i, j) == X[i][j])
              for i in range(DIMENSION) for j in range(DIMENSION) ]


oh_no_constraint = cells_c + blue_1 + blue_val

## Blank instance of a 5x5 grid
            # ((-1, -1, -1, -1, -1),
            # (-1, -1, -1, -1, -1),
            # (-1, -1, -1, -1, -1),
            # (-1, -1, -1, -1, -1),
            # (-1, -1, -1, -1, -1))
## Blank instance of a 9x9 grid
#  ((-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1),
#   (-1, -1, -1, -1, -1, -1, -1, -1, -1))

instance =   ((1, -1, -1, 4, -1, -1, -1, -1, 8),
              (-1, -1, 0, 4, -1, -1, -1, 3, 7),
              (5, -1, -1, -1, -1, -1, -1, -1, -1),
              (-1, -1, -1, 7, 7, -1, -1, -1, 6),
              (-1, 5, -1, -1, -1, -1, -1, -1, -1),
              (-1, 0, -1, 3, -1, 4, -1, -1, 9),
              (-1, -1, -1, 7, -1, -1, 8, 6, -1),
              (-1, 6, -1, -1, 6, -1, 7, 5, -1),
              (4, -1, 0, -1, -1, -1, -1, -1, 2))

instance_c = [ If(instance[i][j] == -1,
                  True,
                  X[i][j] == instance[i][j])
               for i in range(DIMENSION) for j in range(DIMENSION) ]

#print(X)

s = Solver()
s.add(oh_no_constraint + instance_c)
if s.check() == sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(DIMENSION) ]
          for i in range(DIMENSION) ]
    print_matrix(r)
else:
    print("failed to solve")
