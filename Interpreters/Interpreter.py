from scipy.fft import fft, ifft, fftfreq
from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from utils.percentage_for import percentage_for


#############################################
#               INTERPRETER                 #
#############################################

# Interpreter es una clase madre, de la cual heredan las clases Encrypy y Decrypt.
# Notamos que ambos procesos utilizan funciones similares tales como:
#       Leer archivo de audio original (read_wav)
#       Aplicar transformacion FFT (FFT)
#       Aplicar algoritmo de encripcion y desencriptacion --> Llamar a funcion Encrypt de objeto Algoritmo (BLOWFISH_Cipher , AES_Cipher)
#       Aplicar transformacion inversa IFFT
#       Guardar archivo de audio .wav

# Funciones
#   IFFT --> Realiza transformada inversa de Fourier.
#       Recibe:
#       Devuelve:
#   FFT --> Realiza transformada de Fourier.
#       Recibe:
#       Devuelve:
#   Encrypt --> Aplica algoritmo de encriptaicon
#       Recibe:
#       Devuelve:
#   Decrypt --> Aplica algoritmo de encriptaicon
#       Recibe:
#       Devuelve:
#   Create_Wav --> Guarda seÃ±al de audio en el tiempo a .wav
#       Recibe:
#       Devuelve:


class Interpreter:
    def __init__(self):
        self.time_samples = None
        self.FFT_Array = None
        self.FFT_Freq = None
        self.FFT_ASCII = None
        self.IFFT_Array = None
        self.signal = None
        self.time = None
        self.fs = None
        self.Max2Norm = None

    # ESTAS FUNCIONES ESTARAN EN ENCRYPT Y DECRYPT PQ DEPENDE DE SI
    # ENCIPTAMOS O DECIFRAMOS MULTIPLICAMOS O DIVIDIOMS LOS SAMPLES POR 5 AL LEER WAV O CREAR WAV
    # def Read_Wav(self,path):
    #     sample_rate, samples = wav.read(path)
    #     self.fs = sample_rate
    #     #return samples[:,0]
    #     return samples

    # def create_Wav(self, signal, name_wav ):
    #     print("\nsignal que llega a Create Wav\n",signal)
    #     wav.write( name_wav, self.fs, signal.astype(np.int16))
    #     sample_rate, samples = wav.read(name_wav)
    #     print("\nImprimo lo que guarde en el wav nuevo\n",samples)
    #

    def FFT(self):         # No recibe nada y devuelve la fft en formato matriz cuya columna 0
                                   # es la parte real y la col 1 es la parte imaginaria
                                   # First we read .wav file and apply Fast Fourier Transform
        self.FFT_Array = fft(self.signal)
        print("\nWav after FFT\n", self.FFT_Array)

        # Posible error: fftfreq(N, 1/SAMPLE RATE)

        self.FFT_Freq = fftfreq(len(self.signal), 1/self.fs)

        for i in range(len(self.FFT_Freq)):
            if (self.FFT_Freq[i] > 2000):
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






    def IFFT(self,FFT_Array):
        #Recbie FFTa de encrypt_to_FFT_ASCII o FFT de byte_toFFT  --> SON ARRAYS

        # First we decode bytes to array of complex numbers to apply IFFT
        array_imag = np.zeros(len(FFT_Array), complex)
        print(len(FFT_Array))
        for fil in range(len(FFT_Array)):
            array_imag[fil] = complex(FFT_Array[fil][0], FFT_Array[fil][1])

        #PLOTEO FFT
        #plt.plot(self.FFT_Freq, np.abs(self.FFT_Array))
        #plt.shot()

        conjugado = np.conj(array_imag)
        conj = np.flip(conjugado)
        array_imag = np.append(array_imag, conj)

        self.IFFT_Array = ifft(array_imag).real
        return self.IFFT_Array
        # Last we save results from IFFT to a .wav file



    def get_max2norm(self):
        return self.Max2Norm

    def get_FFTfreq(self):
        return self.FFT_Freq