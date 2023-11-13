class Task:
    def __init__(self):
        self.SUCCESS = 'SUCCESS'
        self.FAILURE = 'FAILURE'
        self.RUNNING = 'RUNNING'

    def execute(self, npc=None):
        print("Execute Task")
        return self.FAILURE
    

#####################################
#            Compositions           #
#####################################

class Sequence(Task):
    def __init__(self, tasks:Task):
        self.__subtasks = tasks

    def execute(self, npc):
        for task in self.__subtasks:
            status = task.execute(npc)
            if status != self.SUCCESS:
                return status
        return self.SUCCESS
    
    
class Selection(Task):
    def __init__(self, tasks:Task):
        self.__subtasks = tasks

    def execute(self, npc):
        for task in self.__subtasks:
            status = task.execute(npc)
            if status != self.FAILURE:
                return status
        return self.FAILURE
