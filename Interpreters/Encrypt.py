from Interpreters.Interpreter import Interpreter
import numpy as np
from scipy.io import wavfile as wav
from scipy.fft import fft, ifft, fftfreq

import simpleaudio as sa

from AES.aes import AES_Cipher
from Blowfish.blowfish import BLOWFISH_Cipher

from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from utils.percentage_for import percentage_for

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
        self.Process = None
        self.FTT = None
        self.FFTe = None

    def encrypt_wav(self, wav, process_type, mode, NombreArchivoNuevo):
        self.signal = self.Read_Wav(wav)   #Si bien la funcion devuelve un samples, esa informacion ya esta guardada en self.fs
        print("\nencrypt wav señal original\n",self.signal)
        FFT = self.FFTEncrypt()

        FFTb = self.FFT_to_byte(FFT)

        self.Encrypt_Process(process_type,mode)

        self.cipher.Encrypt(self.Process, FFTb)

        if(self.cipher.status == 1):
            print("La encriptacion fue correcta")
            FFTe = self.cipher.cipher_data
            print("\nEcrypt: FFTe\n", FFTe[:20])
            FFTa = self.Encrypt_to_FFT_ASCII(FFTe)
            self.key = self.cipher.get_key()
            wav_answer = self.IFFTEncrypt(FFTa)
            self.create_Wav(wav_answer, NombreArchivoNuevo+ ".wav")
            f = open(NombreArchivoNuevo + ".txt","w+")
            f.write(str(len(self.FFT_Freq)) + "\n" + str(self.Max2Norm.real) + "\n")

            if self.Process == Blowfish.MODE_CBC or self.Process == AES.MODE_CBC:
                Cipher_IV_str = self.get_CipherIV()
                f.write(Cipher_IV_str + "\n")

            f.close()


        elif(self.cipher.status == 0):
            print("La encriptacion no fue correcta")

    def Encrypt_Process(self, algoritmo,mode):
        if algoritmo == "BLOW":
            self.cipher = BLOWFISH_Cipher()
            if (mode == "ecb"):
                self.Process = Blowfish.MODE_ECB
            elif (mode == "cbc"):
                self.Process = Blowfish.MODE_CBC

        elif algoritmo == "AES":
            self.cipher = AES_Cipher()
            if (mode == "ecb"):
                self.Process = AES.MODE_ECB
            elif (mode == "cbc"):
                self.Process = AES.MODE_CBC
        else:
            print("pone un algoritmo crack")


    def FFT_to_byte(self, matrix):
        self.data_matrix_FFT = matrix           # Recibe de funcion Interpreter.FFT()
        string = ""

        for fil in range(len(self.data_matrix_FFT[:,0])):
            for col in range(len(self.data_matrix_FFT[0, :])):


                if (self.data_matrix_FFT[fil][col] >= 0):
                    string = string + "+" + str(abs(self.data_matrix_FFT[fil][col]))
                else:
                    string = string + "-" + str(abs(self.data_matrix_FFT[fil][col]))

            percentage_for(fil, len(self.data_matrix_FFT))

        FFTb = bytes(string, 'ascii')
        print("\nEncrypt: FFTb\n",FFTb[:20])
        return FFTb


    def Encrypt_to_FFT_ASCII(self, FFTe):  # Recibe transformada de Fourier encriptada
                                           # Devuelve array de FFT interpretando valores ASCII
        self.data_byte_enc = FFTe
        str_data = self.data_byte_enc.decode("latin-1")

        resto = (len(str_data)) % 2  # Vemos si es par
        if (resto):
            str_data += '\0'         # Si tengo un largo impar, le agrego un caracter nulo que despues voy a descartar

        self.data_matrix_FFT = np.array([[0, 0]])
        print(len(str_data))
        for i in range(0, len(str_data), 2):
            word1 = str_data[i]
            word1_ASCII = ord(word1)
            word2 = str_data[i + 1]
            word2_ASCII = ord(word2)
            percentage_for(i, len(str_data))

            pre_answer = np.array([[int(word1_ASCII), int(word2_ASCII)]])
            if (i == 0):
                self.data_matrix_FFT = pre_answer
            else:
                self.data_matrix_FFT = np.append(self.data_matrix_FFT, pre_answer, axis=0)
        FFTa = self.data_matrix_FFT
        print("\nEncrypt: FFTa\n",FFTa)
        return FFTa


    def Read_Wav(self,path):
        sample_rate, samples = wav.read(path)
        self.fs = sample_rate
        # if len(samples[0]) > 1:
        #     return samples[:,0]
        # elif len(samples[0] == 1):
        #     return samples
        return samples

    def create_Wav(self, signal, name_wav ):
        print("\nSamples que llegan a Create Wav en encrypt\n",signal)
        self.Max2Norm = signal.max()
        print("\nEncrypt: Max de señal encriptada creada\n",self.Max2Norm)
        signalNorm = signal.astype(np.float32)/self.Max2Norm
        wav.write( name_wav, self.fs, signalNorm.real)


    def IFFTEncrypt(self,FFTa):
        #Recbie FFTa de encrypt_to_FFT_ASCII --> SON ARRAYS
        # First we decode bytes to array of complex numbers to apply IFFT
        array_imag = np.zeros(len(FFTa), complex)
        for fil in range(len(FFTa)):
            array_imag[fil] = complex(FFTa[fil][0], FFTa[fil][1])

        print("\n Array Image\n", array_imag)

        self.IFFT_Array = ifft(array_imag)
        array_ans = np.append(self.IFFT_Array.real, self.IFFT_Array.imag)
        self.IFFT_Array = array_ans

        print("\nEncrypt: Samples 2 encrypted wav\n",self.IFFT_Array)
        # FFTDECRYPT(IFFT ENCRYPT (FFTa)) = FFTa

        return self.IFFT_Array
        # Last we save results from IFFT to a .wav file


    def FFTEncrypt(self):         # No recibe nada y devuelve la fft en formato matriz cuya columna 0
                                   # es la parte real y la col 1 es la parte imaginaria
                                   # First we read .wav file and apply Fast Fourier Transform
        self.FFT_Array = fft(self.signal)
        print("\nEncrypt: Wav after FFT\n", self.FFT_Array)

        # Posible error: fftfreq(N, 1/SAMPLE RATE)

        self.FFT_Freq = fftfreq(len(self.signal), 1/self.fs)
        w = 0
        for i in range(len(self.FFT_Freq)):
            if (self.FFT_Freq[i] > 500):
                w = i
                break
        self.FFT_Array = self.FFT_Array[:w]
        # Last we encode FFT array of complex numbers to bytes to use the encryption algorithms
        matrix = np.zeros((len(self.FFT_Array), 2))
        for fil in range(len(self.FFT_Array)):
            for col in range(len(matrix[0])):
                if col == 0:
                    matrix[fil][col] = self.FFT_Array[fil].real
                if col == 1:
                    matrix[fil][col] = self.FFT_Array[fil].imag
            percentage_for(fil, len(self.FFT_Array))

        print("\nEncrypt: FFT limitada en freq\n", self.FFT_Array)
        return matrix

 ###### GUI ######

    def play_signal_O(self, signal):
        signal *= 32767 / np.max(np.abs(signal))
        signal = signal.astype(np.int16)
        self.play_O = sa.play_buffer(signal, 1, 2, int(self.fs))
        # self.play.wait_done()

    def play_O(self):
        if self.signal is not None:
            self.play_signal_O(self.signal)

    def pause_reproduction_O(self):
        # if self.play.isplaying() and self.play is not None:
        if self.play_O is not None:
            self.play_O.stop()
        else:
            return -1

    def resume_song_O(self, time):
        if self.signal is not None:
            self.play_signal_O(self.signal[int(time * self.fs):])

    ###### Play signal encrypted ( falta guardar la seÃ±al encryptada en la clase )

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


    # GETTERS
    def get_key(self):
        return self.cipher.get_key()

    def get_FFTa(self):
        return self.data_matrix_FFT

    def get_IFFTArray(self):
        return self.IFFT_Array

    def get_CipherIV(self):
        if self.Process == Blowfish.MODE_CBC or self.Process == AES.MODE_CBC:
            print("\nCIPHER IV DIRECTO", self.cipher.get_cipher_IV())
            return self.cipher.get_cipher_IV()
        else:
            print("\n \n ERROR no es CBC \n \n")
            return "Error"