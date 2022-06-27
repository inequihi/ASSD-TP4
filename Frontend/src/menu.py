from PyQt5.QtWidgets import *
from Frontend.src.ui.menu import Ui_Menu
from pathlib import Path
from Frontend.counter import *
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


        #COUNTER
        self.first_time_O = 0
        self.pausa_O = False
        self.play_O = True
        self.pause_O = True

        self.first_time_E = 0
        self.pausa_E = False
        self.play_E = True
        self.pause_E = True

        self.first_time_E2 = 0
        self.pausa_E2 = False
        self.play_E2 = True
        self.pause_E2 = True

        self.first_time_D = 0
        self.pausa_D = False
        self.play_D = True
        self.pause_D = True

        self.counter1 = Counter_O(self, 4)      #FALTA DURACION DE LA CANCICON
        self.counter2 = Counter_E(self, 4)
        self.counter3 = Counter_E2(self, 4)
        self.counter4 = Counter_D(self, 4)



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
        if self.first_time_O == 0:
            self.pausa_O = False
            self.counter1.start_thread()
            self.first_time_O = 1
        if self.pausa_O == False:
            self.counter1.pause_loop = False
            #plau spmg in back
        else:
            if(self.play_O):
                self.pause_O = True
                self.counter1.pause_loop = False
                #resume song back
                self.play_O = False

    def pause_song_O(self):
        print("PAUSA ORIGINAL")
        if (self.pause_O):
            self.pausa_O = True
            self.play_O = True
            self.pause_O = False
            self.counter1.pause_loop = True
            #paise in back

    def reset_song_O(self):
        print("STOP ORIGINAL")
        self.play_O = False
        self.pausa_O = False
        self.pause_O = True
        self.counter1.reset_loop = True
        self.counter1.start()
        #pausame reproduccion en el back
        #pone play en el back



    def play_song_E(self):
        print("PLAY ENCRYPTADO")
        if self.first_time_E == 0:
            self.pausa_E = False
            self.counter2.start_thread()
            self.first_time_E = 1
        if self.pausa_E == False:
            self.counter2.pause_loop = False
            # plau spmg in back
        else:
            if (self.play_E):
                self.pause_E = True
                self.counter2.pause_loop = False
                # resume song back
                self.play_E = False

    def pause_song_E(self):
        print("PAUSA ENCRYPTADO")
        if (self.pause_E):
            self.pausa_E = True
            self.play_E = True
            self.pause_E = False
            self.counter2.pause_loop = True
            #paise in back

    def reset_song_E(self):
        print("STOP ENCRYPTADO")
        self.play_E = False
        self.pausa_E = False
        self.pause_E = True
        self.counter2.reset_loop = True
        self.counter2.start()
        # pausame reproduccion en el back
        # pone play en el back




    def play_song_E2(self):
        print("PLAY ENCRYPTADO CARGADO")
        if self.first_time_E2 == 0:
            self.pausa_E2 = False
            self.counter3.start_thread()
            self.first_time_E2 = 1
        if self.pausa_E2 == False:
            self.counter3.pause_loop = False
            # plau spmg in back
        else:
            if (self.play_E2):
                self.pause_E2 = True
                self.counter3.pause_loop = False
                # resume song back
                self.play_E2 = False

    def pause_song_E2(self):
        print("PAUSA ENCRYPTADO CARGADO")
        if (self.pause_E2):
            self.pausa_E2 = True
            self.play_E2 = True
            self.pause_E2 = False
            self.counter3.pause_loop = True
            #paise in back

    def reset_song_E2(self):
        print("STOP ENCRYPTADO CARGADO")
        self.play_E2 = False
        self.pausa_E2 = False
        self.pause_E2 = True
        self.counter3.reset_loop = True
        self.counter3.start()
        # pausame reproduccion en el back
        # pone play en el back




    def play_song_D(self):
        print("PLAY DESENCRYPTADO")
        if self.first_time_D == 0:
            self.pausa_D = False
            self.counter4.start_thread()
            self.first_time_D = 1
        if self.pausa_D == False:
            self.counter4.pause_loop = False
            # plau spmg in back
        else:
            if (self.play_D):
                self.pause_D = True
                self.counter4.pause_loop = False
                # resume song back
                self.play_D = False


    def pause_song_D(self):
        print("PAUSA DESENCRYPTADO")
        if (self.pause_D):
            self.pausa_D = True
            self.play_D = True
            self.pause_D = False
            self.counter4.pause_loop = True
            #paise in back

    def reset_song_D(self):
        print("STOP DESENCRYPTADO")
        self.play_D = False
        self.pausa_D = False
        self.pause_D = True
        self.counter4.reset_loop = True
        self.counter4.start()
        # pausame reproduccion en el back
        # pone play en el back