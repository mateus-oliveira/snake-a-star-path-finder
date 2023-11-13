from turtle import Pen, Screen
from snake.pathfinder import find_path
from snake.utils import *


class Node:
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__color = color
        
        pen = Pen()
        pen.hideturtle()
        pen.penup()
        pen.shape('sprite')
        pen.color(color)
        pen.speed('fastest')
        self.__pen = pen

    @property
    def position(self):
        return self.__x, self.__y

    # setters
    def set_position(self, x, y):
        self.__x = x
        self.__y = y

    def clear(self):
        self.__pen.clear()

    def draw(self):
        x, y = self.position
        pen = self.__pen
        pen.clear()
        pen.goto(x*CELL_SIZE, y*CELL_SIZE)
        pen.stamp()


class Snake:
    def __init__(self, x=0, y=0):
        self.__color = 'green'
        self.__body = [Node(x, y, self.__color), Node(x, y, self.__color)]

    @property
    def coords(self):
        return [node.position for node in self.__body]

    @property
    def head(self):
        return self.__body[-1].position

    def __add_node_to_body(self):
        last_node = self.__body[-1]
        x, y = last_node.position
        self.__body.append(Node(x, y, self.__color))

    def draw(self):
        for node in self.__body:
            node.draw()

    def set_position(self, x, y):
        for node in self.__body:
            node.set_position(x, y)

    def move(self, path):
        if path:
            for x, y in path:                      
                head = self.__body[0]
                head.set_position(x, y)
                self.__body.pop(0)
                self.__body.append(head)
                head.draw()
 
            self.__add_node_to_body()


class Obstacles:
    def __init__(self):
        self.__wall = []

    @property
    def coords(self):
        return [node.position for node in self.__wall]

    def add(self, x, y):
        self.__wall.append(Node(x, y, 'black'))

    def draw(self):
        for node in self.__wall:
            node.draw()


class Scene:
    def __init__(self):
        self._screen = Screen()
        self._screen.setup(SCREEN_SIZE, SCREEN_SIZE)
        self._screen.register_shape('sprite', ((0, 0), (0, CELL_SIZE), (CELL_SIZE, CELL_SIZE), (CELL_SIZE, 0)))
        self._screen.title('Snake Game with A* Algorithm')
        self._screen.onscreenclick(self.__on_click_left,  1)
        self._screen.onscreenclick(self.__on_click_right, 2)

        self._snake = Snake()
        self._obstacles = Obstacles()

        self._grid = []
        
        self._food = None


    def __is_valid_move(self, x, y):
        if (x, y) not in self._snake.coords + self._obstacles.coords:
            return True
        return False

    def __on_click_left(self, x, y):
        if self._food:
            return
        
        i, j = screen_to_grid(x, y)
        x, y = grid_to_screen_sized(i, j)
        
        if not self.__is_valid_move(x, y) or self._grid[i][j] == BLOCKED_CHAR:
            print(f'invalid movement: ({x}, {y})')
            return

        self._grid[i][j] = FOOD_CHAR
        self._food = Node(x, y, 'red')
        self._food.draw()

        x_snake, y_snake = self._snake.head
        i_snake, j_snake = screen_sized_to_grid(x_snake, y_snake)

        path = [
            grid_to_screen_sized(_i, _j)
            for _i, _j in find_path(
                grid=self._grid,
                start=(i_snake, j_snake),
                goal=(i, j),
            )
        ]
        self._snake.move(path)
        
        self._food.clear()
        self._food = None

        x, y = path[0]
        i, j = screen_sized_to_grid(x, y)
        self._grid[i][j] = EMPTY_CHAR

        self.print_grid()

    def __on_click_right(self, x, y):
        print('botão direito')

    # TODO - remover
    def print_grid(self):
        for line in self._grid:
            print(' '.join(line))

    def run(self, path):
        grid = []
        with open(path, 'r') as file:
            for line in file:
                row = list(line.strip())
                grid.append(row)

            for i, row in enumerate(grid):
                for j, col in enumerate(row):
                    if col == SNAKE_CHAR:
                        x, y = grid_to_screen_sized(i, j)
                        self._snake.set_position(x, y)
                    elif col == WALL_CHAR:
                        x, y = grid_to_screen_sized(i, j)
                        self._obstacles.add(x, y)
                        
            self._grid = grid
            
            self._snake.draw()
            self._obstacles.draw()


def main():
    level = Scene()
    level.run('snake/level.txt')


if __name__ == '__main__':
    main()
