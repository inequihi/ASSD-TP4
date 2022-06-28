from Interpreters.Interpreter import Interpreter
import numpy as np
from scipy.io import wavfile as wav

from AES.aes import AES_Cipher
from Blowfish.blowfish import BLOWFISH_Cipher

from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish

##################################
#           DECRYPT              #
##################################
# Funciones
#   FFT_ASCII_to_encrypt --> Parsea array FFT con contenido ASCII a string de bytes encriptado
#   Byte_to_FFT --> Parsea el string the bytes desencriptado y lo acomoda en un FFT array

class Decrypt(Interpreter):
    def __init__(self):
        self.time_samples = None
        self.data_byte_enc = None  # b'%5yu/223?'
        self.data_matrix_FFT = None  # [ [1,2] [3,4] ]
        self.cipher = None
        self.signal_decrypt= None
        self.fft_decrypt = None

    def decrypt_wav(self, wav, algoritmo, KEY, MODE, cipher_IV=None) :
        # Como dividi por 5 en encrypt, para llegar a los ascii correctos debo multiplicar por 5
        self.signal = self.Read_Wav(wav)
        self.data_matriz_FTT = self.FFT()
        self.data_byte_enc = self.FFT_ASCII_to_encrypt(self.data_matriz_FTT)
        self.fft_decrypt =self.Byte_to_FFT(self.Decrypt_Process(algoritmo, KEY, MODE, self.data_byte_enc, cipher_IV))
        self.signal_decrypt = self.IFFT( self.fft_decrypt)
        self.create_Wav(self.signal_decrypt, wav)

    def Read_Wav(self,path):
        sample_rate, samples = wav.read(path)
        print("\nSamples recibidas por decrypt:\n",samples)
        print("\nSamples*5 recibidas por decrypt:\n",samples*5)
        self.fs = sample_rate
        #return samples[:,0]
        return samples

    def create_Wav(self, signal, name_wav ):
        print("\nsignal que llega a Create Wav\n",signal)
        wav.write( name_wav, self.fs, signal.astype(np.int16))
        sample_rate, samples = wav.read(name_wav)
        print("\nImprimo lo que guarde en el wav nuevo\n",samples)


    def Decrypt_Process(self,algoritmo, KEY, mode, cipher_data, cipher_IV=None):
        if algoritmo == "BLOW":
            self.cipher = BLOWFISH_Cipher()
        elif algoritmo == "AES":
            self.cipher = AES_Cipher()
        else:
            print("pone un algoritmo crack")

        if (mode == "ecb"):
            self.Process = Blowfish.MODE_ECB
            self.cipher.Decrypt(KEY, Blowfish.MODE_ECB, cipher_data)
        elif (mode == "cbc"):
            self.Process = Blowfish.MODE_CCB
            self.cipher.Decrypt(KEY, Blowfish.MODE_CCB, cipher_data)

        return self.cipher.plain_data

    def FFT_ASCII_to_encrypt(self, FFTa):
        # Recibe FFTa de Interpreter.FFT
        # Devuelve FFTe para aplicar algoritmo de desencriptacion
        self.data_matrix_FFT = FFTa
        str_answer = ""
        for i in range(0, len(self.data_matrix_FFT)):
            for j in range(0, len(self.data_matrix_FFT[i])):
                str_answer += (chr(int(self.data_matrix_FFT[i][j])))

        b_answer = str_answer.encode("latin-1")

        self.data_byte_enc = b_answer
        FFTe = self.data_byte_enc
        return FFTe  # b'%5yu/223?'


    def Byte_to_FFT(self, byte_fft):
        i = 0
        k = 0
        size_FFT_arr = 0
        string_fft = byte_fft.decode(encoding='utf-8')
        # Obtengo size del FFT array
        mas = string_fft.count('+')  # +1+2+4+2-33+4 --> +1+2j  +4+2k -33+4j   --> 6 signos --> 3 elementos de matriz
        menos = string_fft.count('-')
        if ((mas + menos) % 2):
            print("ERROR EN TAMAÑO DE BYTE_FFT")
        else:
            size_FFT_arr = int((mas + menos) / 2)

        # Creo array de FFT
        FFT = np.zeros((size_FFT_arr, 2))
        indexTemp = 0

        for i in range(size_FFT_arr):

            for j in range(2):
                signoTemp = ""
                StringTemp = ""
                # Primer for loop para obtener un stirng de un numero
                for k in range(indexTemp, len(string_fft) - 1):
                    if ((string_fft[k] == '+') or (string_fft[k] == '-')):  # Interpreto el signo si lo encuentro
                        signoTemp = string_fft[k]
                        print("Signo temp:", signoTemp)

                    if ((string_fft[k + 1] != '+') and (string_fft[k + 1] != '-')):  # Sumo 1 pq el indice k empieza en el signo
                        StringTemp += string_fft[k + 1]
                        print(StringTemp)
                    else:
                        indexTemp = k + 1
                        break
                FFT[i][j] = float(StringTemp)  # Asigno valores
                if (signoTemp == '-'):
                    FFT[i][j] = FFT[i][j] * -1
        return FFT
