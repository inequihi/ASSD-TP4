from Interpreters.Interpreter import Interpreter
import numpy as np
from scipy.io import wavfile as wav
from scipy.fft import fft, ifft, fftfreq


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

    def encrypt_wav(self, wav, process_type, mode):
        self.signal = self.Read_Wav(wav)   #Si bien la funcion devuelve un samples, esa informacion ya esta guardada en self.fs
        print("\nencrypt wav señal original\n",self.signal)
        FFT = self.FFT()

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
            self.create_Wav(wav_answer, "encriptado.wav")

        elif(self.cipher.status == 0):
            print("La encriptacion no fue correcta")

    def Encrypt_Process(self, algoritmo,mode):
        if algoritmo == "BLOW":
            self.cipher = BLOWFISH_Cipher()

        elif algoritmo == "AES":
            self.cipher = AES_Cipher()
        else:
            print("pone un algoritmo crack")

        if (mode == "ecb"):
            self.Process = Blowfish.MODE_ECB
        elif (mode == "cbc"):
            self.Process = Blowfish.MODE_CBC


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
        print("\nEncrypt: FFTb\n",FFTb)
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


    def create_Wav(self, signal, name_wav ):
        print("\nSamples que llegan a Create Wav en encrypt\n",signal)
        self.Max2Norm = signal.max()
        signalNorm = signal.astype(np.float32)/self.Max2Norm
        wav.write( name_wav, self.fs, signalNorm)
        sample_rate, samples = wav.read(name_wav)
        print("\nEncrypt: Wav creado por encrypt\n",samples)

    def Read_Wav(self,path):
        sample_rate, samples = wav.read(path)
        self.fs = sample_rate
        #return samples[:,0]
        return samples


    def IFFTEncrypt(self,FFT_Array):
        #Recbie FFTa de encrypt_to_FFT_ASCII --> SON ARRAYS

        # First we decode bytes to array of complex numbers to apply IFFT
        array_imag = np.zeros(len(FFT_Array), complex)
        print(len(FFT_Array))
        for fil in range(len(FFT_Array)):
            array_imag[fil] = complex(FFT_Array[fil][0], FFT_Array[fil][1])

        #PLOTEO FFT
        #plt.plot(self.FFT_Freq, np.abs(self.FFT_Array))
        #plt.shot()

        self.IFFT_Array = ifft(array_imag).real
        print("\nEncrypt: Samples 2 encrypted wav\n",self.IFFT_Array)
        return self.IFFT_Array
        # Last we save results from IFFT to a .wav file

    # GETTERS
    def get_key(self):
        return self.cipher.get_key()

    def get_FFTa(self):
        return self.data_matrix_FFT


