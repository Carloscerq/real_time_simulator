class Algorithm:
    def __init__(self, tasks, quantum):
        self.tasks = tasks
        self.quantum = quantum

    def schedule(self):
        raise NotImplementedError("Subclasses devem implementar o método schedule")