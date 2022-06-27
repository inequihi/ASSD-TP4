from PyQt5.QtWidgets import *
from Frontend.src.ui.menu import Ui_Menu
from pathlib import Path
import Frontend.src.ui.notes50x50
import Frontend.src.ui.play
import Frontend.src.ui.pause
import Frontend.src.ui.stop


class MenuWindow (QWidget, Ui_Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        #TOOLBARS
        self.MplWidget.show_toolbar(self.Toolbar1)
        self.MplWidget_2.show_toolbar(self.verticalLayout_4)
        self.MplWidget_5.show_toolbar(self.Toolbar1_3)
        self.MplWidget_6.show_toolbar(self.verticalLayout_12)


        #HIDES
        self.label_key_tittle.hide()
        self.label_KEY.hide()


        #BUTTONS
        #encryptacion
        self.Button_Upload_Original.clicked.connect(self.get_message_file)
        self.Button_Encrypt.clicked.connect(self.encrypt_message)
        self.Button_CreateWAV_Encrypt.clicked.connect(self.create_encrypy_wav)
        #desencryptacion
        self.Button_Upload_Encrypt.clicked.connect(self.get_encrypt_file)
        self.Button_Desencrypt.clicked.connect(self.desencrypt_message)
        self.Button_CreateWAV_Desencrypt.clicked.connect(self.descreate_encrypy_wav)





    def get_message_file(self):
        print("upload")
        filename = QFileDialog.getOpenFileNames()
        self.original_path = filename[0][0]
        self.original_path_name = Path(self.original_path)


    def get_encrypt_file(self):
        print("upload")
        filename = QFileDialog.getOpenFileNames()
        self.encrypt_path = filename[0][0]
        self.encrypt_path_name = Path(self.encrypt_path)



    def encrypt_message(self):
        print("Encrypt")
        self.label_key_tittle.show()

        self.label_KEY.show()

    def create_encrypy_wav(self):
        print("CREO WAV ENCRYPTADO")



    def desencrypt_message(self):
        print("Encrypt")
        self.label_key_tittle.show()

        self.label_KEY.show()

    def descreate_encrypy_wav(self):
        print("CREO WAV ENCRYPTADO")