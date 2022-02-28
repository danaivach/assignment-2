# Exercise 2: Automated Planning

A partial implementation of a STRIPS-like planner in Python. The the planner solves a problem based on a domain, where both the problem and the domain are defined in PDDL. 

### Requirements
The project requires [Python](https://www.python.org/) >= 3.6.

### How to run the project 
You can run the script `plan.py` with Python 3 for solving a problem defined in PDDL.
You can specify the following arguments:
- positional arguments:
  - `domain`: the file path of the domain defined in PDDL
  - `problem`: the file path of the problem defined in PDDL

- optional arguments:
  - `-s {astar,wastar,gbf,bfs,ehs,ids,sat}`: the search algorithm from A*, weighted A*, greedy best first, breadth first, enforced hillclimbing, iterative deepening, sat solve (default: bfs)

```
python3 plan.py [-s {astar,wastar,gbf,bfs,ehs,ids,sat}] [domain] problem
```
For example, to run the planner with the A* search algorithm:
```
python3 plan.py -s astar blocks-domain.pddl blocks-problem.pddl
```
