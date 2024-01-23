from settings import *
from copy import deepcopy

class Problem:
    def __init__(self, game):
        self.game = game
        self.start_state = ((self.game.layout.pac_pos[1], self.game.layout.pac_pos[0]), self.game.layout.food)

    def startState(self):
        return self.start_state
    
    def goalStateTest(self, state):
        achived = True
        for row in state[1]:
            if True in row:
                achived = False
                break
            
        return achived

    def getSuccessors(self, state):
        successors = []
        for direction in [right, left, up, down]:
            x, y = state[0]
            next_x = int(x + direction.x)
            next_y = int(y + direction.y)

            if not self.game.layout.walls[next_y][next_x]:
                nextFood = deepcopy(state[1])
                nextFood[next_y][next_x] = False
                successors.append((((next_x, next_y), nextFood), direction))
                print((x, y),(next_x, next_y))
        return successors

def DFS(problem):
    stack = []
    visited = []
    successor = problem.startState()
    stack.append((successor, []))
    ans = []

    while len(stack) != 0:
        state, actions = stack.pop()

        if state in visited:
            continue

        if problem.goalStateTest(state):
            ans = actions
            break

        visited.append(state)

        for nextState, action in problem.getSuccessors(state):
            if nextState not in visited:
                stack.append((nextState, actions + [action]))

    return ans

def BFS(problem):
    queue = []
    visited = []
    successor = problem.startState()
    queue.insert(0, (successor, []))
    ans = []

    while len(queue) != 0:
        state, actions = queue.pop()

        if state in visited:
            continue

        if problem.goalStateTest(state):
            ans = actions
            break

        visited.append(state)

        for nextState, action in problem.getSuccessors(state):
            if nextState not in visited:
                queue.insert(0, (nextState, actions + [action]))

    return ans