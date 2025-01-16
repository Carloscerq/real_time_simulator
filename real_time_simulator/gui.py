import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import threading

class GUI:
    app: QApplication
    current_window: QWidget
    pos_x: int
    pos_y: int
    width: int
    height: int

    def __init__(
        self,
        window_title: str = "Simulador Tempo Real",
        window_geometry: tuple[int, int, int, int] = (100, 100, 800, 600),
        algorithms: dict = None,
    ):
        """
        Inicializa os valores necessários para começar a utilizar a GUI
        """
        self.app = QApplication([])
        self.current_window = QWidget()
        self.current_window.setWindowTitle(window_title)
        self.current_window.setGeometry(*window_geometry)
        self.current_window.setMinimumSize(800, 600)
        self.pos_x, self.pos_y, self.width, self.height = window_geometry

        self.algorithms = algorithms or {}
        self.tasks = []
        self.running = False

        self.layout = QVBoxLayout(self.current_window)
        self.setup_ui()

    def setup_ui(self):
        # Título principal
        title = QLabel(f"<h1>Simulador de Tempo Real</h1>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        # Canvas para o gráfico
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas, stretch=3)

        # Área de entrada de tarefas e lista de tarefas
        task_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Tarefa,Tempo de execução (ex: T1,10)")
        input_layout.addWidget(self.task_input)

        add_task_button = QPushButton("Adicionar Tarefa")
        add_task_button.clicked.connect(self.add_task)
        input_layout.addWidget(add_task_button)

        task_layout.addLayout(input_layout)

        self.task_list = QListWidget()
        task_layout.addWidget(self.task_list)

        remove_task_button = QPushButton("Remover Tarefa Selecionada")
        remove_task_button.clicked.connect(self.remove_task)
        task_layout.addWidget(remove_task_button)

        self.layout.addLayout(task_layout, stretch=2)

        # Seleção de algoritmo
        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(self.algorithms.keys())
        self.layout.addWidget(self.algorithm_selector)

        # Entrada de quantum
        self.quantum_input = QLineEdit()
        self.quantum_input.setPlaceholderText("Quantum (ex: 4)")
        self.layout.addWidget(self.quantum_input)

        # Botão de iniciar
        start_button = QPushButton("Iniciar Escalonamento")
        start_button.clicked.connect(self.start_schedule)
        self.layout.addWidget(start_button)

    def add_task(self):
        task_text = self.task_input.text()
        if "," in task_text:
            task_id, burst_time = task_text.split(",")
            try:
                burst_time = int(burst_time)
                self.tasks.append((task_id.strip(), burst_time))
                self.task_input.clear()
                self.update_task_list()
            except ValueError:
                pass  # Ignora entradas inválidas

    def remove_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_text = selected_item.text()
            task_id = task_text.split(":")[0].strip()
            self.tasks = [task for task in self.tasks if task[0] != task_id]
            self.update_task_list()

    def update_task_list(self):
        self.task_list.clear()
        for task_id, burst_time in self.tasks:
            self.task_list.addItem(f"{task_id}: {burst_time} unidades de tempo")

    def start_schedule(self):
        if not self.running and self.tasks:
            algorithm_name = self.algorithm_selector.currentText()
            quantum_text = self.quantum_input.text()

            try:
                quantum = int(quantum_text)
                scheduler = self.algorithms[algorithm_name](self.tasks, quantum)
                self.running = True
                threading.Thread(target=self.run_scheduler, args=(scheduler.schedule,)).start()
            except ValueError:
                pass  # Ignora valores de quantum inválidos

    def run_scheduler(self, scheduler_callback):
        for schedule in scheduler_callback():
            self.plot_schedule(schedule)

    def plot_schedule(self, schedule):
        ax = self.canvas.figure.subplots()
        ax.clear()

        for i, (task_id, start, end) in enumerate(schedule):
            ax.broken_barh([(start, end - start)], (0, 10), facecolors=f"C{i}")

        ax.set_xlabel("Tempo")
        ax.set_ylabel("Tarefa")
        ax.set_ylim(0, 15)
        ax.set_xlim(0, max(end for _, _, end in schedule) + 5)
        ax.grid(True)

        self.canvas.draw()

    def run(self):
        self.current_window.showMaximized()
        sys.exit(self.app.exec())
