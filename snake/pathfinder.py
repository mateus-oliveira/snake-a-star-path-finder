from snake.constants import *

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost


def heuristic(node, goal_node):
    # Distância de Manhattan como heurística
    return abs(node.x - goal_node.x) + abs(node.y - goal_node.y)


def _find_path(grid, start: tuple, goal: tuple):
    start_node = Node(start[1], start[0], SNAKE_CHAR)
    goal_node = Node(goal[1], goal[0], FOOD_CHAR)

    heuristic_values = [[heuristic(Node(x, y, grid[y][x]), goal_node) for x in range(len(grid[0]))] for y in range(len(grid))]
    
    open_set = {start_node}
    closed_set = set()

    while open_set:
        current_node = min(open_set, key=lambda x: x.f_cost)
        open_set.remove(current_node)
        closed_set.add((current_node.x, current_node.y))

        if current_node.value == FOOD_CHAR:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = current_node.x + i, current_node.y + j
            if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid) and grid[new_y][new_x] != WALL_CHAR and (new_x, new_y) not in closed_set:
                neighbor = Node(new_x, new_y, grid[new_y][new_x])
                neighbor.g_cost = current_node.g_cost + 1
                neighbor.h_cost = heuristic_values[new_y][new_x]
                neighbor.parent = current_node

                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None



def find_path(grid, start:tuple, goal:tuple):
    path = _find_path(grid, start, goal)
    if path is None:
        return None
    return [(y, x) for x, y in path]
