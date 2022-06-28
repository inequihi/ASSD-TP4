from Interpreters.Interpreter import Interpreter
from utils.percentage_for import percentage_for

import numpy as np
from scipy.io import wavfile as wav
from scipy.fft import fft, ifft, fftfreq


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
        self.tamañoSignalOriginal = None

    def decrypt_wav(self, wav, algoritmo, KEY, MODE, cipher_IV=None) :
        print("\n --------------------- DECRYPT ---------------------- \n")
        self.signal = self.Read_Wav(wav)
        data_matriz_FTT = self.data_matrix_FFT
        self.data_byte_enc = self.FFT_ASCII_to_encrypt(data_matriz_FTT)
        self.fft_decrypt =self.Byte_to_FFT(self.Decrypt_Process(algoritmo, KEY, MODE, self.data_byte_enc, cipher_IV))
        self.signal_decrypt = self.IFFTDecrypt(self.fft_decrypt)
        self.create_Wav(self.signal_decrypt, "desencriptado.wav")

    def Read_Wav(self,path):
        sample_rate, samples = wav.read(path)
        print("\nDecrypt: Samples from encrypted wav\n",samples*self.Max2Norm)
        self.fs = sample_rate
        #return samples[:,0]
        return samples*self.Max2Norm

    def create_Wav(self, signal, name_wav ):
        print("\nsignal que llega a Create Wav\n",signal)
        self.Max2Norm = signal.max()
        wav.write( name_wav, self.fs, signal.astype(np.float32)/self.Max2Norm)
        sample_rate, samples = wav.read(name_wav)
        print("\nDecrypt: Sampes 2 decrypted wav\n",samples)


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
            self.Process = Blowfish.MODE_CBC
            self.cipher.Decrypt(KEY, Blowfish.MODE_CBC, cipher_data,cipher_IV)

        return self.cipher.plain_data

    def FFT_ASCII_to_encrypt(self, FFTa):
        # Recibe FFTa de Interpreter.FFT
        # Devuelve FFTe para aplicar algoritmo de desencriptacion
        self.data_matrix_FFT = FFTa
        print("FFTa",self.data_matrix_FFT)
        str_answer = ""
        for i in range(0, len(self.data_matrix_FFT)):
            for j in range(0, len(self.data_matrix_FFT[i])):
                str_answer += (chr(int(self.data_matrix_FFT[i][j])))

        b_answer = str_answer.encode("latin-1")

        self.data_byte_enc = b_answer
        FFTe = self.data_byte_enc
        print("\nDecrypt:FFTe\n",FFTe[:20])
        return FFTe  # b'%5yu/223?'


    def Byte_to_FFT(self, byte_fft):
        print("\nDecrypt: FFTb\n",byte_fft)
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
                        #print("Signo temp:", signoTemp)

                    if ((string_fft[k + 1] != '+') and (string_fft[k + 1] != '-')):  # Sumo 1 pq el indice k empieza en el signo
                        StringTemp += string_fft[k + 1]
                        #print(StringTemp)
                    else:
                        indexTemp = k + 1
                        break
                FFT[i][j] = float(StringTemp)  # Asigno valores
                if (signoTemp == '-'):
                    FFT[i][j] = FFT[i][j] * -1
        print("\nDecrypt: FFT\n",FFT)
        return FFT


    def FFTDecrypt(self):         # No recibe nada y devuelve la fft en formato matriz cuya columna 0
                                   # es la parte real y la col 1 es la parte imaginaria
                                   # First we read .wav file and apply Fast Fourier Transform
        self.FFT_Array = fft(self.signal)
        print("\nDecrypt: Wav after FFT\n", self.FFT_Array)

        # Last we encode FFT array of complex numbers to bytes to use the encryption algorithms
        matrix = np.zeros((len(self.FFT_Array), 2))
        for fil in range(len(self.FFT_Array)):
            for col in range(len(matrix[0])):
                if col == 0:
                    matrix[fil][col] = self.FFT_Array[fil].real
                if col == 1:
                    matrix[fil][col] = self.FFT_Array[fil].imag
            percentage_for(fil, len(self.FFT_Array))
        print("\nDecrypt: FFTa\n", matrix)

        return matrix





    def IFFTDecrypt(self,FFT_Array):
        #Recbie FFTa de encrypt_to_FFT_ASCII o FFT de byte_toFFT  --> SON ARRAYS

        # First we decode bytes to array of complex numbers to apply IFFT
        array_imag = np.zeros(len(FFT_Array), complex)
        for fil in range(len(FFT_Array)):
            array_imag[fil] = complex(FFT_Array[fil][0], FFT_Array[fil][1])

        n = self.tamañoSignalOriginal - len(array_imag)*2
        ceros = np.zeros(n)

        conjugado = np.conj(array_imag)
        conj = np.flip(conjugado)

        array_imag = np.append(array_imag, ceros)

        array_imag = np.append(array_imag, conj)

        self.IFFT_Array = ifft(array_imag).real
        return self.IFFT_Array
        # Last we save results from IFFT to a .wav file


    # SETTERS
    def set_Max2Norm(self,max2norm):
        self.Max2Norm = max2norm

    def set_FFTa(self, FFTa):
        self.data_matrix_FFT = FFTa

    def set_TamañoSignalOriginal(self,tamaño):
        self.tamañoSignalOriginal = tamaño