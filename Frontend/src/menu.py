from PyQt5.QtWidgets import *
from Frontend.src.ui.menu import Ui_Menu
from pathlib import Path
import Frontend.src.ui.notes50x50
import Frontend.src.ui.play
import Frontend.src.ui.pause
import Frontend.src.ui.stop
import Frontend.src.ui.copy


class MenuWindow (QWidget, Ui_Menu):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        #TOOLBARS
        self.MplWidget.show_toolbar(self.Toolbar1_2)
        self.MplWidget_2.show_toolbar(self.verticalLayout_10)
        self.MplWidget_5.show_toolbar(self.Toolbar1_3)
        self.MplWidget_6.show_toolbar(self.verticalLayout_14)


        #HIDES
        self.label_key_tittle.hide()
        self.label_KEY.hide()
        self.pushButton_copy.hide()
        self.label_incorrect_D.hide()
        self.label_incorrect_E.hide()

        #RADIO BUTTON
        self.radioButton_AES.clicked.connect(self.put_green_red_encrypt)
        self.radioButton_Blowfish.clicked.connect(self.put_green_red_encrypt)


        #TEXT IN
        self.lineEdit_key.textEdited.connect(self.put_green_red_desencrypt)


        #BUTTONS
        #encryptacion
        self.Button_Upload_Original.clicked.connect(self.get_message_file)
        self.Button_Encrypt.clicked.connect(self.encrypt_message)
        self.Button_CreateWAV_Encrypt.clicked.connect(self.create_encrypy_wav)
        self.pushButton_copy.clicked.connect(self.copy)
        #desencryptacion
        self.Button_Upload_Encrypt.clicked.connect(self.get_encrypt_file)
        self.Button_Desencrypt.clicked.connect(self.desencrypt_message)
        self.Button_CreateWAV_Desencrypt.clicked.connect(self.descreate_encrypy_wav)

        #RECORDING BUTTONS
        self.pushButton_play_O.clicked.connect(self.play_song_O)
        self.pushButton_pausa_O.clicked.connect(self.pause_song_O)
        self.pushButton_rec_O.clicked.connect(self.reset_song_O)

        self.pushButton_play_E.clicked.connect(self.play_song_E)
        self.pushButton_pausa_E.clicked.connect(self.pause_song_E)
        self.pushButton_rec_E.clicked.connect(self.reset_song_E)

        self.pushButton_play_E2.clicked.connect(self.play_song_E2)
        self.pushButton_pausa_E2.clicked.connect(self.pause_song_E2)
        self.pushButton_rec_E2.clicked.connect(self.reset_song_E2)

        self.pushButton_play_D.clicked.connect(self.play_song_D)
        self.pushButton_pausa_D.clicked.connect(self.pause_song_D)
        self.pushButton_rec_D.clicked.connect(self.reset_song_D)





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
        if (self.radioButton_AES.isChecked()) == 0 and (self.radioButton_Blowfish.isChecked()) == 0:
            self.label_incorrect_E.setText("Incorrect: Algorithm was no chosen. Please choose one to continue.")
            self.label_incorrect_E.show()
        else:
            self.label_incorrect_E.hide()
            self.label_key_tittle.show()
            self.pushButton_copy.show()

            self.label_KEY.show()

    def create_encrypy_wav(self):
        print("CREO WAV ENCRYPTADO")



    def desencrypt_message(self):
        print("Desencrypt")
        if len(self.lineEdit_key.text()) == 0:
            self.label_incorrect_D.setText("Incorrect: The key is empty. Please fill the line.")
            self.label_incorrect_D.show()
        else:
            self.label_incorrect_D.hide()


    def descreate_encrypy_wav(self):
        print("CREO WAV DESENCRYPTADO")

    def copy(self):
        self.CtrlC = QApplication.clipboard()
        self.CtrlC.clear(mode=self.CtrlC.Clipboard)
        self.CtrlC.setText(self.label_KEY.text(), mode=self.CtrlC.Clipboard)
        print("COPY")


    def put_green_red_encrypt(self):
        self.Button_Encrypt.setStyleSheet("background: green;\n"
                                                 "color: white;")

    def put_green_red_desencrypt(self):
        if len(self.lineEdit_key.text()) == 0:
            self.Button_Desencrypt.setStyleSheet("background: red;\n"
                                                 "color: white;")
        else:
            self.Button_Desencrypt.setStyleSheet("background: green;\n"
                                                 "color: white;")


    #RECORDING BUTTONS

    def play_song_O(self):
        print("PLAY ORIGINAL")

    def pause_song_O(self):
        print("PAUSA ORIGINAL")

    def reset_song_O(self):
        print("STOP ORIGINAL")



    def play_song_E(self):
        print("PLAY ENCRYPTADO")

    def pause_song_E(self):
        print("PAUSA ENCRYPTADO")

    def reset_song_E(self):
        print("STOP ENCRYPTADO")




    def play_song_E2(self):
        print("PLAY ENCRYPTADO CARGADO")

    def pause_song_E2(self):
        print("PAUSA ENCRYPTADO CARGADO")

    def reset_song_E2(self):
        print("STOP ENCRYPTADO CARGADO")




    def play_song_D(self):
        print("PLAY DESENCRYPTADO")

    def pause_song_D(self):
        print("PAUSA DESENCRYPTADO")

    def reset_song_D(self):
        print("STOP DESENCRYPTADO")