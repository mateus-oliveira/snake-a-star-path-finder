class Task:
    def __init__(self, tasks: list = None):
        self.SUCCESS = 'SUCCESS'
        self.FAILURE = 'FAILURE'
        self.RUNNING = 'RUNNING'

    def execute(self, npc):
        print("Execute a Task")
        return self.FAILURE
    

#####################################
#            Compositions           #
#####################################

class Sequence(Task):
    def __init__(self, tasks: list = None):
        super().__init__(tasks)
        self.__subtasks = tasks

    def execute(self, npc):
        for task in self.__subtasks:
            status = task.execute(npc)
            if status != self.SUCCESS:
                return status
        return self.SUCCESS
    
    
class Selection(Task):
    def __init__(self, tasks: list = None):
        super().__init__(tasks)
        self.__subtasks = tasks

    def execute(self, npc):
        for task in self.__subtasks:
            status = task.execute(npc)
            if status != self.FAILURE:
                return status
        return self.FAILURE


#################################
#       SNAKE BEHAVIOR          #
#################################

class VerticalMoveUp(Task):
    def execute(self, npc):
        npc.vertical_waiting_move()
        return self.SUCCESS


class VerticalMoveDown(Task):
    def execute(self, npc):
        npc.vertical_waiting_move(direction=-1)
        return self.SUCCESS


class IsSeeingAFood(Task):
    def execute(self, npc):
        if npc.food_exists():
            return self.SUCCESS
        return self.FAILURE


class FindPathToFood(Task):
    def execute(self, npc):
        if npc.path_found():
            return self.SUCCESS
        if npc.find_path():
            return self.RUNNING
        return self.FAILURE


class FinallyEat(Task):
    def execute(self, npc):
        if npc.move():
            return self.RUNNING
        return self.SUCCESS


def create_behavior():
    vertical_movement_up = VerticalMoveUp()
    vertical_movement_down = VerticalMoveDown()

    waiting = Sequence([vertical_movement_up, vertical_movement_down])

    is_seeing_a_food = IsSeeingAFood()
    find_path_to_food = FindPathToFood()
    finally_eat = FinallyEat()

    eat = Sequence([is_seeing_a_food, find_path_to_food, finally_eat])

    behavior = Selection([eat, waiting])

    return behavior
