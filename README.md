# 0h_n0_SATSolver
A SAT solver for the puzzle game 0h n0 implemented with Z3 in python

## Use Instructions
### Dependencies:
In order to use the solver, you will need the z3-solver package installed you can install it by running:
```
pip install z3-solver
```
### Using the solver
Set the dimension to the size of the board (for example, 6 for a 6x6). Then set the board instance for the puzzle you'd like to solve. here is an example:
```
instance =   ((1, -1, -1, 4, -1, -1, -1, -1, 8),
              (-1, -1, 0, 4, -1, -1, -1, 3, 7),
              (5, -1, -1, -1, -1, -1, -1, -1, -1),
              (-1, -1, -1, 7, 7, -1, -1, -1, 6),
              (-1, 5, -1, -1, -1, -1, -1, -1, -1),
              (-1, 0, -1, 3, -1, 4, -1, -1, 9),
              (-1, -1, -1, 7, -1, -1, 8, 6, -1),
              (-1, 6, -1, -1, 6, -1, 7, 5, -1),
              (4, -1, 0, -1, -1, -1, -1, -1, 2))
```
-1 is an empty cell, 0 is a red cell, and a positive integer represents a blue cell that must see exactly that number of blue cells.

Running the program will output a 2D array representing the solution of the given instance.

Program was tested in python version 3.7 and above.
