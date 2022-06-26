from src.menu import MenuWindow
from PyQt5.QtWidgets import QApplication
import src.ui.nota
import src.ui.play
import src.ui.pause
import src.ui.stop

if __name__ == '__main__':

    app = QApplication([])
    window = MenuWindow()
    window.show()

    app.exec()