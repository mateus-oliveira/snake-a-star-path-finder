from turtle import Pen, Screen
from snake.pathfinder import find_path
from snake.behavior_tree import create_behavior
from snake.utils import *


SCREEN = Screen()
SCREEN.setup(SCREEN_SIZE, SCREEN_SIZE)
SCREEN.register_shape('sprite', ((0, 0), (0, CELL_SIZE), (CELL_SIZE, CELL_SIZE), (CELL_SIZE, 0)))
SCREEN.title('NPC Snake')

PEN = Pen()
PEN.hideturtle()
PEN.penup()
PEN.shape('sprite')
PEN.speed('fastest')


class Node:
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        pen = PEN.clone()
        pen.color(color)
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
    def __init__(self, scene, x=0, y=0):
        self.__color = 'green'
        self.__body = [Node(x, y, self.__color), Node(x, y, self.__color)]
        self.scene = scene
        self.path = None
        self.__behavior = create_behavior()

    @property
    def coords(self):
        return [node.position for node in self.__body]

    def path_found(self):
        return self.path is not None
    
    def __add_node_to_body(self):
        last_node = self.__body[-1]
        x, y = last_node.position
        self.__body.append(Node(x, y, self.__color))

    def food_exists(self):
        return self.scene.food is not None

    def draw(self):
        for node in self.__body:
            node.draw()

    def set_position(self, x, y):
        for node in self.__body:
            node.set_position(x, y)

    def find_path(self):
        if self.path_found():
            return False
        x_snake, y_snake = self.__body[-1].position
        i_snake, j_snake = screen_sized_to_grid(x_snake, y_snake)

        x_food, y_food = self.scene.food.position
        i_food, j_food = screen_sized_to_grid(x_food, y_food)

        self.path = [
            grid_to_screen_sized(_i, _j)
            for _i, _j in find_path(
                grid=self.scene.grid,
                start=(i_snake, j_snake),
                goal=(i_food, j_food),
            )
        ]

        return True
    
    def vertical_waiting_move(self, direction=1):
        x = -13 if direction > 0 else -14
        for y in range(-14*direction, 14*direction, direction):
            self.__move_head(x, y)
        return True
            
    def move(self):
        if self.path:
            for x, y in self.path:  
                self.__move_head(x, y)
 
            self.__add_node_to_body()
            self.scene.clear_food(self.path)
            self.path = None
            return True
        return False

    def __move_head(self, x, y):                    
        head = self.__body[0]
        head.set_position(x, y)
        self.__body.pop(0)
        self.__body.append(head)
        head.draw()

    def update(self):
        self.__behavior.execute(self)


class Obstacles:
    def __init__(self):
        self.__wall = []
        self.__pen = PEN.clone()
        self.__pen.color('black')

    @property
    def coords(self):
        return self.__wall

    def add(self, x, y):
        self.__wall.append((x, y))

    def draw(self):
        for x, y in self.__wall:
            pen = self.__pen
            pen.goto(x*CELL_SIZE, y*CELL_SIZE)
            pen.stamp()


class Scene:
    def __init__(self):
        self._screen = SCREEN
        self._screen.onscreenclick(self.__on_click)

        self.started = False

        self._snake = Snake(self)
        self._obstacles = Obstacles()

        self._grid = []
        
        self._food = None
        self._screen.ontimer(self.update, 0)

    @property
    def food(self):
        return self._food

    @property
    def grid(self):
        return self._grid

    def __is_valid_move(self, x, y):
        if (x, y) not in self._snake.coords + self._obstacles.coords:
            return True
        return False

    def __on_click(self, x, y):
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

    def clear_food(self, path):
        self._food.clear()
        self._food = None
        x, y = path[0]
        i, j = screen_sized_to_grid(x, y)
        self._grid[i][j] = EMPTY_CHAR
        x, y = path[-1]
        i, j = screen_sized_to_grid(x, y)
        self._grid[i][j] = SNAKE_CHAR


    # TODO - remover
    def print_grid(self):
        for line in self._grid:
            print(' '.join(line))

    def start(self, path):
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

            self.started = True

    def update(self):
        print ('loop')

        if self.started:
            self._snake.update()

        self._screen.update()
        self._screen.ontimer(self.update, 100)


def main():
    level = Scene()
    level.start('snake/level.txt')
    level._screen.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as errors:
        print ("Errors: ", errors)
