from PyQt5.QtWidgets import *
from Frontend.src.ui.menu import Ui_Menu
import Frontend.src.ui.notes50x50
import Frontend.src.ui.play
import Frontend.src.ui.pause
import Frontend.src.ui.stop


class MenuWindow (QWidget, Ui_Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.MplWidget.show_toolbar(self.Toolbar1)
        self.MplWidget_2.show_toolbar(self.verticalLayout_4)
        self.MplWidget_5.show_toolbar(self.Toolbar1_3)
        self.MplWidget_6.show_toolbar(self.verticalLayout_12)