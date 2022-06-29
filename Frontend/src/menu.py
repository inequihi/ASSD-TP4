from PyQt5.QtWidgets import *
from Frontend.src.ui.menu import Ui_Menu
from pathlib import Path
from Frontend.counter import *
import Frontend.src.ui.notes50x50
import Frontend.src.ui.play
import Frontend.src.ui.pause
import Frontend.src.ui.stop
import Frontend.src.ui.copy
from Interpreters.Encrypt import Encrypt
from Interpreters.Decrypt import Decrypt
from utils.graph_FFT import graph_fft


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

        #BACK
        self.encryptor = Encrypt()
        self.decryptor = Decrypt()

        #HIDES
        self.label_key_tittle.hide()
        self.label_KEY.hide()
        self.pushButton_copy.hide()
        self.label_incorrect_D.hide()
        self.label_incorrect_D_2.hide()
        self.label_incorrect_E.hide()
        self.label_copied.hide()
        #self.label.hide()
        #self.label_2.hide()

        #RADIO BUTTON
        self.radioButton_AES.clicked.connect(self.put_green_red_encrypt)
        self.radioButton_Blowfish.clicked.connect(self.put_green_red_encrypt)
        self.radioButton_ECB.clicked.connect(self.put_green_red_encrypt)
        self.radioButton_CBC.clicked.connect(self.put_green_red_encrypt)
        self.radioButton_AES_2.clicked.connect(self.put_green_red_desencrypt)
        self.radioButton_Blowfish_2.clicked.connect(self.put_green_red_desencrypt)
        self.radioButton_ECB_2.clicked.connect(self.put_green_red_desencrypt)
        self.radioButton_CBC_2.clicked.connect(self.put_green_red_desencrypt)


        #TEXT IN
        self.lineEdit_key.textEdited.connect(self.put_green_red_desencrypt)


        #BUTTONS
        #encryptacion
        self.Button_Upload_Original.clicked.connect(self.get_message_file)
        self.Button_Encrypt.clicked.connect(self.encrypt_message)
        self.pushButton_copy.clicked.connect(self.copy)
        #desencryptacion
        self.Button_Upload_Encrypt.clicked.connect(self.get_encrypt_file)
        self.Button_Desencrypt.clicked.connect(self.desencrypt_message)

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

    #FUNCTIONS


    #FUNCTIONS GET FILE UPLOAD
    def get_message_file(self):
        print("upload")
        self.filename_O = QFileDialog.getOpenFileNames()
        self.original_path = self.filename_O[0][0]
        self.original_path_name = Path(self.original_path)


    def get_encrypt_file(self):
        print("upload")
        self.label_key_tittle.hide()
        self.label_KEY.hide()
        self.pushButton_copy.hide()
        self.label_incorrect_D.hide()
        self.label_incorrect_E.hide()
        self.label_copied.hide()
        self.filename_E = QFileDialog.getOpenFileNames()
        self.encrypt_path = self.filename_E[0][0]
        self.encrypt_path_name = Path(self.encrypt_path)


#############################################################################################

    #FUNCTIONS MESSAGES
    def encrypt_message(self):
        print("Encrypt")
        if (self.radioButton_AES.isChecked()) == 0 and (self.radioButton_Blowfish.isChecked()) == 0:
            self.label_incorrect_E.setText("FAIL: Algorithm was no chosen. Please choose one to continue.")
            self.label_incorrect_E.show()
        else:
            if self.radioButton_AES.isChecked() == 1:
                self.algorithm_E = "AES"
            else:
                self.algorithm_E = "BLOW"
            if self.radioButton_ECB == 1:
                self.mode_E = "ecb"
            else:
                self.mode_E = "cbc"
            #self.label.show()
            self.encryptor.encrypt_wav(self.original_path_name, self.algorithm_E, self.mode_E, self.label_new_file_encrypt.text())
            self.label_incorrect_E.hide()
            self.label_key_tittle.show()
            self.pushButton_copy.show()
            self.label_KEY.setText(self.encryptor.get_key().decode('latin-1'))
            self.label_KEY.show()
            self.counter1 = Counter_O(self, self.encryptor.get_original_duration())
            self.counter2 = Counter_E(self, self.encryptor.get_encrypted_duration())
            self.horizontalSlider_Original.setMaximum(int(self.encryptor.get_original_duration()))
            self.horizontalSlider_Encrypt.setMaximum(int(self.encryptor.get_encrypted_duration()))
            graph_fft(self.MplWidget.canvas.ax, self.encryptor.get_o_fft_data())
            self.MplWidget.canvas.draw()
            graph_fft(self.MplWidget_2.canvas.ax, self.encryptor.get_e_fft_data())
            self.MplWidget_2.canvas.draw()
            #self.label.hide()


    def desencrypt_message(self):
        print("Desencrypt")
        if len(self.lineEdit_key.text()) == 0:
            self.label_incorrect_D.setText("FAIL: The key is empty. Please fill the line.")
            self.label_incorrect_D.show()
        elif self.radioButton_AES_2.isChecked() == 0 and self.radioButton_Blowfish_2.isChecked() == 0:
            self.label_incorrect_D_2.setText("FAIL: Fill the buttons.")
            self.label_incorrect_D_2.show()
        elif self.radioButton_ECB_2.isChecked() == 0 and self.radioButton_CBC_2.isChecked() == 0:
            self.label_incorrect_D_2.setText("FAIL: Fill the buttons.")
            self.label_incorrect_D_2.show()
        else:
            self.label_incorrect_D.hide()
            self.label_incorrect_D_2.hide()
            if self.radioButton_AES_2.isChecked() == 1:
                self.algorithm_D = "AES"
            else:
                self.algorithm_D = "BLOW"
            if self.radioButton_ECB_2 == 1:
                self.mode_D = "ecb"
            else:
                self.mode_D = "cbc"
            #self.label_2.show()
            self.decryptor.decrypt_wav(self.encrypt_path_name, self.algorithm_D, self.lineEdit_key.text(), self.mode_D)
            self.counter3 = Counter_E2(self, self.decryptor.get_encrypted_duration())
            self.counter4 = Counter_D(self, self.decryptor.get_original_duration())
            self.horizontalSlider_Encrypt2.setMaximum(int(self.decryptor.get_encrypted_duration()))
            self.horizontalSlider_Desencrypt.setMaximum(int(self.decryptor.get_original_duration()))
            graph_fft(self.MplWidget_5.canvas.ax, self.decryptor.get_e_fft_data())
            self.MplWidget_5.canvas.draw()
            graph_fft(self.MplWidget_6.canvas.ax, self.decryptor.get_o_fft_data())
            self.MplWidget_6.canvas.draw()
            #self.label_2.hide()


#############################################################################################

    #FUNCTION OF COPY
    def copy(self):
        self.CtrlC = QApplication.clipboard()
        self.CtrlC.clear(mode=self.CtrlC.Clipboard)
        self.CtrlC.setText(self.label_KEY.text(), mode=self.CtrlC.Clipboard)
        self.label_copied.show()
        print("COPY")

#############################################################################################

    #FUCTIONS PUT GREEN
    def put_green_red_encrypt(self):
        if self.radioButton_AES.isChecked() == 0 and self.radioButton_Blowfish.isChecked() == 0:
            self.Button_Encrypt.setStyleSheet("background: red;\n"
                                                 "color: white;")
        elif self.radioButton_ECB.isChecked() == 0 and self.radioButton_CBC.isChecked() == 0:
            self.Button_Encrypt.setStyleSheet("background: red;\n"
                                              "color: white;")

        else:
            self.Button_Encrypt.setStyleSheet("background: green;\n"
                                                 "color: white;")


    def put_green_red_desencrypt(self):
        if self.radioButton_AES_2.isChecked() == 0 and self.radioButton_Blowfish_2.isChecked() == 0:
            self.Button_Desencrypt.setStyleSheet("background: red;\n"
                                              "color: white;")
        elif self.radioButton_ECB_2.isChecked() == 0 and self.radioButton_CBC_2.isChecked() == 0:
            self.Button_Desencrypt.setStyleSheet("background: red;\n"
                                              "color: white;")
        else:
            if len(self.lineEdit_key.text()) == 0:
                self.Button_Desencrypt.setStyleSheet("background: red;\n"
                                                     "color: white;")
            else:
                self.Button_Desencrypt.setStyleSheet("background: green;\n"
                                                 "color: white;")

#############################################################################################

    #RECORDING BUTTONS
    def play_song_O(self):
        print("PLAY ORIGINAL")
        if self.first_time_O == 0:
            self.pausa_O = False
            self.counter1.start_thread()
            self.first_time_O = 1
        if self.pausa_O == False:
            self.counter1.pause_loop = False
            self.encryptor.play_O()
        else:
            if(self.play_O):
                self.pause_O = True
                self.counter1.pause_loop = False
                self.encryptor.resume_song_O(self.counter1.play_seconds)
                self.play_O = False

    def pause_song_O(self):
        print("PAUSA ORIGINAL")
        if (self.pause_O):
            self.pausa_O = True
            self.play_O = True
            self.pause_O = False
            self.counter1.pause_loop = True
            self.encryptor.pause_reproduction_O()

    def reset_song_O(self):
        print("STOP ORIGINAL")
        self.play_O = False
        self.pausa_O = False
        self.pause_O = True
        self.counter1.reset_loop = True
        self.counter1.start()
        self.encryptor.pause_reproduction_O()
        self.encryptor.play_O()


    def play_song_E(self):
        print("PLAY ENCRYPTADO")
        if self.first_time_E == 0:
            self.pausa_E = False
            self.counter2.start_thread()
            self.first_time_E = 1
        if self.pausa_E == False:
            self.counter2.pause_loop = False
            self.encryptor.play_E()
        else:
            if (self.play_E):
                self.pause_E = True
                self.counter2.pause_loop = False
                self.encryptor.resume_song_E(self.counter2.play_seconds)
                self.play_E = False

    def pause_song_E(self):
        print("PAUSA ENCRYPTADO")
        if (self.pause_E):
            self.pausa_E = True
            self.play_E = True
            self.pause_E = False
            self.counter2.pause_loop = True
            self.encryptor.pause_reproduction_E()

    def reset_song_E(self):
        print("STOP ENCRYPTADO")
        self.play_E = False
        self.pausa_E = False
        self.pause_E = True
        self.counter2.reset_loop = True
        self.counter2.start()
        self.encryptor.pause_reproduction_E()
        self.encryptor.play_E()




    def play_song_E2(self):
        print("PLAY ENCRYPTADO CARGADO")
        if self.first_time_E2 == 0:
            self.pausa_E2 = False
            self.counter3.start_thread()
            self.first_time_E2 = 1
        if self.pausa_E2 == False:
            self.counter3.pause_loop = False
            self.decryptor.play_E()
        else:
            if (self.play_E2):
                self.pause_E2 = True
                self.counter3.pause_loop = False
                self.decryptor.resume_song_E(self.counter3.play_seconds)
                self.play_E2 = False

    def pause_song_E2(self):
        print("PAUSA ENCRYPTADO CARGADO")
        if (self.pause_E2):
            self.pausa_E2 = True
            self.play_E2 = True
            self.pause_E2 = False
            self.counter3.pause_loop = True
            self.decryptor.pause_reproduction_E()

    def reset_song_E2(self):
        print("STOP ENCRYPTADO CARGADO")
        self.play_E2 = False
        self.pausa_E2 = False
        self.pause_E2 = True
        self.counter3.reset_loop = True
        self.counter3.start()
        self.decryptor.pause_reproduction_E()
        self.decryptor.play_E()




    def play_song_D(self):
        print("PLAY DESENCRYPTADO")
        if self.first_time_D == 0:
            self.pausa_D = False
            self.counter4.start_thread()
            self.first_time_D = 1
        if self.pausa_D == False:
            self.counter4.pause_loop = False
            self.decryptor.play_O()
        else:
            if (self.play_D):
                self.pause_D = True
                self.counter4.pause_loop = False
                self.decryptor.resume_song_O(self.counter4.play_seconds)
                self.play_D = False


    def pause_song_D(self):
        print("PAUSA DESENCRYPTADO")
        if (self.pause_D):
            self.pausa_D = True
            self.play_D = True
            self.pause_D = False
            self.counter4.pause_loop = True
            self.decryptor.pause_reproduction_O()

    def reset_song_D(self):
        print("STOP DESENCRYPTADO")
        self.play_D = False
        self.pausa_D = False
        self.pause_D = True
        self.counter4.reset_loop = True
        self.counter4.start()
        self.decryptor.pause_reproduction_O()
        self.decryptor.play_O()

#############################################################################################