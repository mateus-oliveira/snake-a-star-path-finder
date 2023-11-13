from snake.constants import *


def screen_to_grid(x, y):
    j = int((x + SCREEN_SIZE / 2) // CELL_SIZE)
    i = int((-y + SCREEN_SIZE / 2) // CELL_SIZE)
    return i, j

def grid_to_screen_sized(i, j):
    x = j - int(SCREEN_SIZE / 2) // CELL_SIZE
    y = -i + int(SCREEN_SIZE / 2) // CELL_SIZE
    return x, y

def screen_sized_to_grid(x, y):
    j = x + int(SCREEN_SIZE / 2) // CELL_SIZE
    i = y - int(SCREEN_SIZE / 2) // CELL_SIZE
    return -i, j
