import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow, QMenuBar, QAction, QLabel, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Un simple juego...")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1d1d1e;")  # Fondo oscuro como en el juego

        # Configuración de la fuente para los botones
        font = QFont("Arial", 18, QFont.Bold)

        # Layout principal
        layout = QVBoxLayout()

        # Título de la aplicación
        title = QLabel("Un simple juego", self)
        title.setFont(QFont("Arial", 36, QFont.Bold))
        title.setStyleSheet("color: #02BBE1;")
        title.setAlignment(Qt.AlignCenter)

        # Botones de la interfaz
        self.play_button = QPushButton("Jugar", self)
        self.play_button.setFont(font)
        self.play_button.setStyleSheet("background-color: #02BBE1; color: #fff; border-radius: 10px; padding: 10px;")
        self.play_button.clicked.connect(self.run_game)

        self.options_button = QPushButton("Opciones", self)
        self.options_button.setFont(font)
        self.options_button.setStyleSheet("background-color: #ff6347; color: #fff; border-radius: 10px; padding: 10px;")
        self.options_button.clicked.connect(self.show_options)

        self.exit_button = QPushButton("Salir", self)
        self.exit_button.setFont(font)
        self.exit_button.setStyleSheet("background-color: #ff6347; color: #fff; border-radius: 10px; padding: 10px;")
        self.exit_button.clicked.connect(self.close)

        # Agregar los elementos al layout
        layout.addWidget(title)
        layout.addWidget(self.play_button)
        layout.addWidget(self.options_button)
        layout.addWidget(self.exit_button)

        # Crear un contenedor y asignar el layout
        container = QWidget()
        container.setLayout(layout)

        # Asignar el contenedor a la ventana principal
        self.setCentralWidget(container)

        # Crear la barra de menú
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")
        run_action = QAction("Ejecutar Juego", self)
        run_action.triggered.connect(self.run_game)
        file_menu.addAction(run_action)

        # Pantalla de opciones (simple placeholder)
        self.options_screen = QFrame(self)
        self.options_screen.setStyleSheet("background-color: #1d1d1e; color: #fff;")
        self.options_screen.setGeometry(200, 150, 400, 300)
        self.options_screen.setVisible(False)

        # Agregar texto de opciones
        options_label = QLabel("Opciones de juego", self.options_screen)
        options_label.setStyleSheet("color: #02BBE1; font-size: 24px;")
        options_label.move(100, 50)

        # Opción de volver al menú principal
        back_button = QPushButton("Volver", self.options_screen)
        back_button.setFont(font)
        back_button.setStyleSheet("background-color: #02BBE1; color: #fff; border-radius: 10px; padding: 10px;")
        back_button.move(150, 200)
        back_button.clicked.connect(self.hide_options)

    def run_game(self):
        """Función para ejecutar el script game.py"""
        try:
            subprocess.run(["python", "game.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el juego: {e}")
        except FileNotFoundError:
            print("El archivo game.py no se encuentra en el directorio.")

    def show_options(self):
        """Mostrar la pantalla de opciones"""
        self.options_screen.setVisible(True)
        self.play_button.setVisible(False)
        self.options_button.setVisible(False)
        self.exit_button.setVisible(False)

    def hide_options(self):
        """Ocultar la pantalla de opciones"""
        self.options_screen.setVisible(False)
        self.play_button.setVisible(True)
        self.options_button.setVisible(True)
        self.exit_button.setVisible(True)

def main():
    app = QApplication(sys.argv)

    # Crear la ventana de menú
    window = MenuWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
