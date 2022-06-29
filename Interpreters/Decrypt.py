from Interpreters.Interpreter import Interpreter
from utils.percentage_for import percentage_for

import numpy as np
from scipy.io import wavfile as wav
from scipy.fft import fft, ifft, fftfreq
import cmath

import simpleaudio as sa

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
        self.tamanioSignalOriginal = None
        self.IFFTEncrypt = None
        self.cipher_IV = None


    def decrypt_wav(self, wav, algoritmo, key_str, MODE):
        print("\n --------------------- DECRYPT ---------------------- \n")

        # Leo txt trambolico
        r = open(wav + ".txt", 'r')
        tamanio = int(r.readline())
        max2norm = float(r.readline())
        if MODE == "cbc":
            cipher_IV_str = str(r.readline())
            self.cipher_IV = cipher_IV_str  # CipherIV esta codificado en utf-8
            print("\n self.cipher_IV en decrypt",self.cipher_IV)
        r.close()

        self.tamanioSignalOriginal = tamanio  # Lo voy a usar para crear wav original (IFFTDecrypt)
        self.Max2Norm = max2norm            # Lo voy a usar para read wav

        KEY = key_str.encode('latin-1')  # Recibo la key en string de GUI y la paso a bytes para el algoritmo

        self.signal = self.Read_Wav(wav + ".wav")
        #Aplicamos transformada de fourier a la señal del wav
        self.data_matrix_FFT = self.FFTDecrypt()

        data_matriz_FTT = self.data_matrix_FFT          #Dejamos por posible hardcore

        self.data_byte_enc = self.FFT_ASCII_to_encrypt(data_matriz_FTT)

        self.fft_decrypt =self.Byte_to_FFT(self.Decrypt_Process(algoritmo, KEY, MODE, self.data_byte_enc))
        self.signal_decrypt = self.IFFTDecrypt(self.fft_decrypt)
        self.create_Wav(self.signal_decrypt, wav + "Desencriptado.wav")


    def Read_Wav(self,path):
        sample_rate, samples = wav.read(path)
        self.fs = sample_rate
        return samples*self.Max2Norm


    def create_Wav(self, signal, name_wav ):
        print("\nsignal que llega a Create Wav\n",signal)
        self.Max2Norm = signal.max()
        wav.write( name_wav, self.fs, signal.astype(np.float32)/self.Max2Norm)
        sample_rate, samples = wav.read(name_wav)
        print("\nDecrypt: Sampes 2 decrypted wav\n",samples)


    def Decrypt_Process(self,algoritmo, KEY, mode, cipher_data):
        if algoritmo == "BLOW":
            self.cipher = BLOWFISH_Cipher()
            if (mode == "ecb"):
                self.Process = Blowfish.MODE_ECB
                self.cipher.Decrypt(KEY, Blowfish.MODE_ECB, cipher_data)
            elif (mode == "cbc"):
                self.Process = Blowfish.MODE_CBC
                self.cipher.Decrypt(KEY, Blowfish.MODE_CBC, cipher_data, self.cipher_IV)

        elif algoritmo == "AES":
            self.cipher = AES_Cipher()
            if (mode == "ecb"):
                self.Process = AES.MODE_ECB
                self.cipher.Decrypt(KEY, AES.MODE_ECB, cipher_data)
            elif (mode == "cbc"):
                self.Process = AES.MODE_CBC
                self.cipher.Decrypt(KEY, AES.MODE_CBC, cipher_data, self.cipher_IV)
        else:
            print("pone un algoritmo crack")
        return self.cipher.plain_data


    def FFT_ASCII_to_encrypt(self, FFTa):
        # Recibe FFTa de Interpreter.FFT
        # Devuelve FFTe para aplicar algoritmo de desencriptacion
        self.data_matrix_FFT = FFTa

        str_answer = ""
        for i in range(0, len(FFTa)):
            for j in range(0, len(FFTa[i])):
                y = FFTa[i][j]
                x = (int(round(FFTa[i][j])))
                str_answer += str(chr(x))

        b_answer = str_answer.encode("latin-1")

        self.data_byte_enc = b_answer
        FFTe = self.data_byte_enc
        print("\nDecrypt:FFTe\n",FFTe[:20])
        return FFTe  # b'%5yu/223?'


    def Byte_to_FFT(self, byte_fft):
        print("\nDecrypt: FFTb\n",byte_fft[:20])
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
        # OJO es diferente a FFTEncrypt pq aca no reducimos el tamaño de la señal
        # en frecuencia. Necesitamos si o si todos los datos.

        #self.FFT_Array = fft(self.signal)
        print("\nIFFTEncrypt recibida por Decrypt:\n",self.signal)

        half_array = int((len(self.signal)) / 2)
        FFTa_Decrypt = np.empty(1)
        for i in range(half_array):
            arr = FFTa_Decrypt
            value = complex(self.signal[i], self.signal[i + half_array])

            FFTa_Decrypt = np.append(arr, value)

        self.FFT_Array = fft(FFTa_Decrypt[1:])
        print(self.FFT_Array)
        FFTa_Decrypt = np.empty(1)
        for i in range(len(self.FFT_Array)):
            arr = FFTa_Decrypt
            value = complex(self.FFT_Array[i].real, self.FFT_Array[i].imag)
            FFTa_Decrypt = np.append(arr, value)

        self.FFT_Array = FFTa_Decrypt[1:]
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

        n = self.tamanioSignalOriginal - len(array_imag) * 2
        ceros = np.zeros(n)

        conjugado = np.conj(array_imag)
        conj = np.flip(conjugado)

        array_imag = np.append(array_imag, ceros)
        array_imag = np.append(array_imag, conj)

        self.IFFT_Array = ifft(array_imag).real
        return self.IFFT_Array
        # Last we save results from IFFT to a .wav file

    ######## GUI ###########

    def play_signal_O(self, signal):
        signal *= 32767 / np.max(np.abs(signal))
        signal = signal.astype(np.int16)
        self.play_O = sa.play_buffer(signal, 1, 2, int(self.fs))
        # self.play.wait_done()

    def play_O(self):
        if self.signal_decrypt is not None:
            self.play_signal_O(self.signal_decrypt)

    def pause_reproduction_O(self):
        # if self.play.isplaying() and self.play is not None:
        if self.play_O is not None:
            self.play_O.stop()
        else:
            return -1

    def resume_song_O(self, time):
        if self.signal_decrypt is not None:
            self.play_signal_O(self.signal_decrypt[int(time * self.fs):])

    ###### Play signal encrypted

    def play_signal_E(self, signal):
        signal *= 32767 / np.max(np.abs(signal))
        signal = signal.astype(np.int16)
        self.play_E = sa.play_buffer(signal, 1, 2, int(self.fs))
        # self.play.wait_done()

    def play_E(self):
        if self.signal is not None:
            self.play_signal_O(self.signal)

    def pause_reproduction_E(self):
        # if self.play.isplaying() and self.play is not None:
        if self.play_E is not None:
            self.play_E.stop()
        else:
            return -1

    def resume_song_E(self, time):
        if self.signal is not None:
            self.play_signal_E(self.signal[int(time * self.fs):])


    # SETTERS
    def set_FFTa(self, FFTa):
        self.data_matrix_FFT = FFTa


    def set_IFFTEncrypt(self,ifftenc):
        self.IFFTEncrypt = ifftenc