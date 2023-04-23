from __future__ import print_function
from ortools.linear_solver import pywraplp


def main():
    '''
    Assignment Problem.
    Six workers, divided in two teams, each can perform at most two tasks.
    Team 1: 0,1,4
    Team 2: 2,3,5

    Constraints:
    1. Each worker is assigned to at most 1 task
    2. Each task is assigned to exactly 1 worker
    3. Worker 0 has to be assigned to either tas 2 or 3
    '''

    # initialize your solver, you can use the 'CLP' solver
    # CLP = CLP Linear Programming
    solver = pywraplp.Solver.CreateSolver('CLP')
    # initialize the cost matrix

    cost = [[45, 50, 90, 80],
            [40, 70, 55, 70],
            [130, 100, 40, 90],
            [45, 80, 120, 50],
            [40, 110, 80, 95],
            [55, 90, 70, 110]]

    # declare the two teams and team_max

    team_1 = [0, 1, 4]
    team_2 = [2, 3, 5]

    # declare num_workers and num_tasks and assign them the correct value
    num_workers = len(cost)
    num_tasks = len(cost[0])

    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0, 1, '')

    # Objective function
    objective_terms = []

    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(cost[i][j]*x[i, j])

    solver.Minimize(solver.Sum(objective_terms))

    '''
    Same as:
    solver.Minimize(solver.Sum([cost[i][j] * x[i, j] for i in range(num_workers)
                                for j in range(num_tasks)]))
    '''

    # Constraints

    # Each worker is assigned to at most 1 task.

    for i in range(num_workers):
        solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) <= 1)

    # Each task is assigned to exactly one worker.

    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) == 1)

    # Worker 0 has to be assigned to either task 2 or 3

    # Each team takes on two tasks.

    # solve the model

    print('Total cost = ', solver.Objective().Value())
    print()
    for i in range(num_workers):
        for j in range(num_tasks):
            if x[i, j].solution_value() > 0:
                print('Worker %d assigned to task %d.  Cost = %d' % (
                      i,
                      j,
                      cost[i][j]))

    print()
    print("Time = ", solver.WallTime(), " milliseconds")


if __name__ == '__main__':
    main()
