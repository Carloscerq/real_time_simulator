import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel


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
        window_geometry: tuple[int, int, int, int] = (100, 100, 450, 300),
    ):
        """
        Inicia os valores necessarios para comecar a utilizar a GUI
        """
        self.app = QApplication([])
        self.current_window = QWidget()
        self.current_window.setWindowTitle(window_title)
        self.current_window.setGeometry(*window_geometry)
        self.pos_x, self.pos_y, self.width, self.height = window_geometry

    def set_initial_window(self):
        title = QLabel(f"<h1>Simulador de tempo real<h1>", parent=self.current_window)
        title.move(int(self.width / 10), 20)

    def run(self):
        self.current_window.show()
        sys.exit(self.app.exec())
