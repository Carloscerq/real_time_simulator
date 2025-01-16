from real_time_simulator.gui import GUI
from real_time_simulator.algorithms.round_robin import RoundRobin

if __name__ == "__main__":
    algorithms = {
        "Round Robin": RoundRobin
    }

    gui = GUI(algorithms=algorithms)
    gui.run()
