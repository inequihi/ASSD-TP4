from scipy.fft import fft, ifft
from scipy.io import wavfile as wav
import numpy as np

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
#   Save_Wav --> Guarda señal de audio en el tiempo a .wav
#       Recibe:
#       Devuelve:


class Interpreter:
    # En el constructor deberia recibir un parametro que sea el tipo de algoritmo que se va a utilizar
    # para asi crear un objeto del mismo y usar sus funciones de encriptar y desencriptar
    def __init__(self):
        self.time_samples = None
        self.FFT_Array = None
        self.FFT_ASCII = None
        self.IFFT_Array = None

    def FFT(self, signal):         # Recibe path de canción y devuelve la fft en formato matriz cuya columna 0
                                   # es la parte real y la col 1 es la parte imaginaria
                                   # First we read .wav file and apply Fast Fourier Transform
        self.FFT_Array = fft(signal)
        # Last we encode FFT array of complex numbers to bytes to use the encryption algorithms
        matrix = np.zeros((len(self.FFT_Array), 2))
        for fil in range(len(self.FFT_Array)):
            for col in range(len(matrix[0])):
                if (col == 0):
                    matrix[fil][col] = self.FFT_Array[fil].real
                if (col == 1):
                    matrix[fil][col] = self.FFT_Array[fil].imag
        return matrix

    def IFFT(self,Encrypted_FFT):
        # First we decode bytes to array of complex numbers to apply IFFT
        FFT_Array = self.Bytes2Array(Encrypted_FFT)
        array_imag = np.zeros(len(FFT_Array[:][0]), complex)
        for fil in range(len(FFT_Array[:][0])):
            array_imag[fil] = complex(FFT_Array[fil][0], FFT_Array[fil][1])

        self.IFFT_Array = ifft(array_imag)

        # Last we save results from IFFT to a .wav file
