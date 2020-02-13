# crossword-generator

Generator of random crosswords using a SAT solver

## Problem

This script generates a random crossword using a given set of words. The main strategy for solving the problem is using a SAT Solver and Python 3 is the language used to generate the input for the SAT Solver, read the output and print the crossword.

## SAT Solver

### What is a SAT Solver
The Boolean SATisfiability Problem is the problem of finding a solution of a boolean forumla (specifically a CNF). This is an NP-complete problem, but some algorithms exist that can sometimes solve this problem in a short time using different kinds of heuristics.

### What is a CNF
A CNF (Conjunctive Normal Form) is a conjunction of disjunctions of boolean variables. Some examples of CNFs that use the variables A, B, C and D are:
- (A ∨ B) ∧ (A ∨ ¬B)
- A ∧ ¬A
- (A ∨ B ∨ ¬C) ∧ (B ¬C ¬D) ∧ D ∧ (D ∨ nA)
The values of the variables that satisfy the equation are the solution of the equation. Each equation can have many solutions (satisfiable), or it may not have any (unsatisfiable). If the equation is satisfiable, the SAT Solver will eventualy find only one of the solutions.

### The SAT Solver used in the project
The SAT Solver used in the project is [MiniSat](http://minisat.se/). This is a free SAT Solver that the script runs on the Unix shell. It can however be easily changed if needed.


## Structure

This is the structure of the project:

[structure1](crossword_structure1.png)

app.py manages the interaction between the different parts of the project. The following image shows the details about how the parts interact:

[structure2](crossword_structure2.png)

### input_generator.py

### cnf_generator.py

### cnf_parser.py

### sat_solver.py

### result_parser.py

### crossword_printer.py

### var_to_string.py

### app.py
