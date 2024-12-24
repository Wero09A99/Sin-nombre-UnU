import sys
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow, QMenuBar, QAction, QLabel, QStackedWidget, QFrame, QComboBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon


class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Un juego simple")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #FDFDFD;")  # Fondo claro y suave

        # Configuración de la fuente para los botones
        font = QFont("Comic Sans MS", 18, QFont.Bold)  # Fuente amigable y redondeada

        # Layout principal
        layout = QVBoxLayout()

        # Título de la aplicación
        title = QLabel("Un juego simple", self)
        title.setFont(QFont("Comic Sans MS", 36, QFont.Bold))
        title.setStyleSheet("color: #FFB6C1;")  # Color rosa pastel
        title.setAlignment(Qt.AlignCenter)

        # Botones de la interfaz
        self.play_button = QPushButton("Jugar", self)
        self.play_button.setFont(font)
        self.play_button.setStyleSheet("background-color: #FFB6C1; color: #fff; border-radius: 20px; padding: 10px;")
        self.play_button.clicked.connect(self.show_level_selector)

        self.options_button = QPushButton("Opciones", self)
        self.options_button.setFont(font)
        self.options_button.setStyleSheet("background-color: #FFB3D9; color: #fff; border-radius: 20px; padding: 10px;")
        self.options_button.clicked.connect(self.show_options)

        self.exit_button = QPushButton("Salir", self)
        self.exit_button.setFont(font)
        self.exit_button.setStyleSheet("background-color: #FFB3D9; color: #fff; border-radius: 20px; padding: 10px;")
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
        self.options_screen.setStyleSheet("background-color: #FDFDFD; color: #000;")
        self.options_screen.setGeometry(200, 150, 400, 300)
        self.options_screen.setVisible(False)

        # Agregar texto de opciones
        options_label = QLabel("Opciones de juego", self.options_screen)
        options_label.setStyleSheet("color: #FFB6C1; font-size: 24px;")
        options_label.move(100, 50)

        # Opción de volver al menú principal
        back_button = QPushButton("Volver", self.options_screen)
        back_button.setFont(font)
        back_button.setStyleSheet("background-color: #FFB6C1; color: #fff; border-radius: 20px; padding: 10px;")
        back_button.move(150, 200)
        back_button.clicked.connect(self.hide_options)

        # Pantalla de selección de nivel
        self.level_selector_screen = QFrame(self)
        self.level_selector_screen.setStyleSheet("background-color: #FDFDFD; color: #000;")
        self.level_selector_screen.setGeometry(200, 150, 400, 300)
        self.level_selector_screen.setVisible(False)

        # Cargar niveles desde el archivo JSON
        self.levels = self.load_levels()

        # Crear un comboBox para seleccionar el nivel
        self.level_combo_box = QComboBox(self.level_selector_screen)
        self.level_combo_box.setStyleSheet("background-color: #FFB6C1; color: #fff; border-radius: 20px; padding: 10px;")
        self.level_combo_box.setGeometry(100, 100, 200, 40)

        # Llenar el ComboBox con los niveles cargados
        for level in self.levels:
            self.level_combo_box.addItem(level["name"])

        # Agregar sombra al comboBox para simular un diseño más suave y amigable
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setXOffset(2)
        shadow_effect.setYOffset(2)
        self.level_combo_box.setGraphicsEffect(shadow_effect)

        # Botón para jugar el nivel seleccionado
        play_level_button = QPushButton("Jugar", self.level_selector_screen)
        play_level_button.setFont(font)
        play_level_button.setStyleSheet("background-color: #FFB6C1; color: #fff; border-radius: 20px; padding: 10px;")
        play_level_button.move(150, 200)
        play_level_button.clicked.connect(self.run_selected_level)

        # Botón de volver
        back_button = QPushButton("Volver", self.level_selector_screen)
        back_button.setFont(font)
        back_button.setStyleSheet("background-color: #FFB3D9; color: #fff; border-radius: 20px; padding: 10px;")
        back_button.move(150, 250)
        back_button.clicked.connect(self.hide_level_selector)

    def load_levels(self):
        """Cargar los niveles desde un archivo JSON"""
        try:
            with open("index_levels.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("No se pudo cargar el archivo index_levels.json.")
            return []

    def show_level_selector(self):
        """Mostrar la pantalla de selección de niveles"""
        self.level_selector_screen.setVisible(True)
        self.play_button.setVisible(False)
        self.options_button.setVisible(False)
        self.exit_button.setVisible(False)

    def hide_level_selector(self):
        """Ocultar la pantalla de selección de niveles"""
        self.level_selector_screen.setVisible(False)
        self.play_button.setVisible(True)
        self.options_button.setVisible(True)
        self.exit_button.setVisible(True)

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

    def run_game(self):
        """Ejecutar el script game.py"""
        try:
            subprocess.run(["python", "game.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el juego: {e}")
        except FileNotFoundError:
            print("El archivo game.py no se encuentra en el directorio.")

    def run_selected_level(self):
        """Ejecutar el nivel seleccionado"""
        selected_level = self.level_combo_box.currentText()  # Obtener el nombre del nivel seleccionado
        level_path = next((level["path"] for level in self.levels if level["name"] == selected_level), None)  # Obtener la ruta del nivel

        if level_path:
            try:
                subprocess.run(["python", level_path], check=True)  # Ejecutar el script del nivel
            except subprocess.CalledProcessError as e:
                print(f"Error al ejecutar el nivel: {e}")
            except FileNotFoundError:
                print(f"El archivo {level_path} no se encuentra en el directorio.")
        else:
            print("Nivel no encontrado.")


def main():
    app = QApplication(sys.argv)

    # Crear la ventana de menú
    window = MenuWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
