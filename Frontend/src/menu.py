from PyQt5.QtWidgets import *
from Frontend.src.ui.menu import Ui_Menu


class MenuWindow (QWidget, Ui_Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)