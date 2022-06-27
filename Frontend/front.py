from src.menu import MenuWindow
from PyQt5.QtWidgets import QApplication
import Frontend.src.ui.notes50x50
import Frontend.src.ui.play
import Frontend.src.ui.pause
import Frontend.src.ui.stop

if __name__ == '__main__':

    app = QApplication([])
    window = MenuWindow()
    window.show()

    app.exec()