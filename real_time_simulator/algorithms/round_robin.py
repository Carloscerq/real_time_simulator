from real_time_simulator.algorithms.Algorithm import Algorithm

class RoundRobin(Algorithm):
    def schedule(self):
        current_time = 0
        schedule = []
        queue = self.tasks[:]

        while queue:
            task = queue.pop(0)
            task_id, burst_time = task

            if burst_time > self.quantum:
                schedule.append((task_id, current_time, current_time + self.quantum))
                current_time += self.quantum
                queue.append((task_id, burst_time - self.quantum))
            else:
                schedule.append((task_id, current_time, current_time + burst_time))
                current_time += burst_time

            yield schedule