from Interpreters.Interpreter import Interpreter
import numpy as np

from AES.aes import AES_Cipher
from Blowfish.blowfish import BLOWFISH_Cipher

from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish

##################################
#           ENCRYPT              #
##################################
# Funciones:
#   FFT_to_byte --> Parsea de matriz FFT a string de bytes, agregando el signo entre cada numero
#   Encrypt_to_FFT_ASCII --> Parsea de encriptado (bytes) a ascii y con ese ascii armo un array FFT

class Encrypt(Interpreter):

    def __init__(self):
        self.time_samples = None
        self.data_byte_enc = None  # b'%5yu/223?'
        self.data_matrix_FFT = None  # [ [1,2] [3,4] ]
        self.cipher = None
        self.FTT = None
        self.FFTe = None

    def Encrypt_Process(self, algoritmo):
        if algoritmo == "BLOW":
            self.cipher = BLOWFISH_Cipher()

        elif algoritmo == "AES":
            self.cipher = AES_Cipher()
        else:
            print("pone un algoritmo crack")


    def FFT_to_byte(self, matrix):
        self.data_matrix_FFT = matrix           # Recibe de funcion Interpreter.FFT()
        string = ""
        for fil in range(len(self.FFT_Array)):
            for col in range(len(self.FFT_Array[0])):
                if (self.FFT_Array[fil][col] >= 0):
                    string = string + "+" + str(self.FFT_Array[fil][col])
                else:
                    string = string + "-" + str(-self.FFT_Array[fil][col])
            print(fil)
        FFTb = bytes(string, 'ascii')
        return FFTb

    def Encrypt_to_FFT_ASCII(self, FFTe):  # Recibe transformada de Fourier encriptada
                                           # Devuelve array de FFT interpretando valores ASCII

        self.data_byte_enc = FFTe
        str_data = self.data_byte_enc.decode("latin-1")

        resto = (len(str_data)) % 2  # Vemos si es par
        if (resto):
            str_data += '\0'         # Si tengo un largo impar, le agrego un caracter nulo que despues voy a descartar

        self.data_matrix_FFT = np.array([[0, 0]])

        for i in range(0, len(str_data), 2):
            word1 = str_data[i]
            word1_ASCII = ord(word1)
            word2 = str_data[i + 1]
            word2_ASCII = ord(word2)

            pre_answer = np.array([[int(word1_ASCII), int(word2_ASCII)]])
            if (i == 0):
                self.data_matrix_FFT = pre_answer
            else:
                self.data_matrix_FFT = np.append(self.data_matrix_FFT, pre_answer, axis=0)
        FFTa = self.data_matrix_FFT

        return FFTa

    def encrypt_wav(self, wav, MODE):


        self.signal = self.Read_Wav(wav)   #Si bien la funcion devuelve un samples, esa informacion ya esta guardada en self.fs

        FFT = self.FFT()

        FFTb = self.FFT_to_byte(FFT)
        if(mode == "ecb"):
            MODE = Blowfish.MODE_ECB
        elif(mode == "cbc"):
            MODE = Blowfish.MODE_CBC

        self.cipher.Encrypt(MODE, FFTb)

        if(self.cipher.status == 1):
            print("La encriptacion fue correcta")
            FFTe = self.cipher.cipher_data
            FFTa = self.Encrypt_to_FFT_ASCII(FFTe)
            self.key = self.cipher.get_key()
            wav_answer = self.IFFT(FFTa)
            self.create_Wav(wav_answer)

        elif(self.cipher.status == 0):
            print("La encriptacion no fue correcta")

