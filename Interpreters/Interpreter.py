from scipy.fft import fft, ifft
from scipy.io import wavfile as wav
import numpy as np
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
#   Create_Wav --> Guarda señal de audio en el tiempo a .wav
#       Recibe:
#       Devuelve:


class Interpreter:
    def __init__(self):
        self.time_samples = None
        self.FFT_Array = None
        self.FFT_ASCII = None
        self.IFFT_Array = None
        self.signal = None
        self.time = None
        self.fs = None
    def Read_Wav(self,path):
        sample_rate, samples = wav.read(path)
        self.fs = sample_rate
        return samples

    def create_Wav(self, signal, name_wav ):
        wav.write( name_wav, self.fs, signal.astype(np.int16))

    def FFT(self):         # No recibe nada y devuelve la fft en formato matriz cuya columna 0
                                   # es la parte real y la col 1 es la parte imaginaria
                                   # First we read .wav file and apply Fast Fourier Transform
        self.FFT_Array = fft(self.signal)
        # Last we encode FFT array of complex numbers to bytes to use the encryption algorithms
        matrix = np.zeros((len(self.FFT_Array), 2))
        for fil in range(len(self.FFT_Array)):
            for col in range(len(matrix[0])):
                if col == 0:
                    matrix[fil][col] = self.FFT_Array[fil][col].real
                if col == 1:
                    matrix[fil][col] = self.FFT_Array[fil][col].imag
            percentage_for(fil, len(self.FFT_Array))
        return matrix

    def IFFT(self,FFT_Array):
        #Recbie FFTa de encrypt_to_FFT_ASCII o FFT de byte_toFFT  --> SON ARRAYS

        # First we decode bytes to array of complex numbers to apply IFFT
        array_imag = np.zeros(len(FFT_Array[:][0]), complex)
        for fil in range(len(FFT_Array[:][0])):
            array_imag[fil] = complex(FFT_Array[fil][0], FFT_Array[fil][1])

        self.IFFT_Array = ifft(array_imag)
        # Last we save results from IFFT to a .wav file

