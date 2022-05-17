from scipy.fft import fft, ifft
from scipy.io import wavfile as wav
import numpy as np

# DATOS MIEMBRO:
    # vector de muestras en el tiempo
    # vector de transformada de fourier (a + bi)
    # FFT_Array
    # FFT_Bytes

# FUNCIONES MIEMBRO:
    # Funcion 1: Leer .wav y hacer FFT
    # Funcion 2: Aplicar IFFT + Convertir a .wav
    # Funcion 3: Parsear FFT de array a bytes
    # Funcion 4: Parsear de Bytes a Array
    # Funcion 5: que sirva para graficar el audio en dominio tiempo y frecuencia y comparar


class FreqDomain:
    def __init__(self):
        self.time_samples = None
        self.FFT_Array = None
        self.FFT_Bytes = None
        self.IFFT_Array = None

    def FFT(self,path):
        # First we read .wav file and apply Fast Fourier Transform
        rate , audio_data = wav.read(path)
        self.FFT_Array = fft(audio_data)

        self.time_samples = audio_data

        # Last we encode FFT array of complex numbers to bytes to use the encryption algorithms
        self.FFT_Bytes = self.Array2Bytes(self.FFT_Array)


    def IFFT(self,Encrypted_FFT):
        # First we decode bytes to array of complex numbers to apply IFFT
        FFT_Array = self.Bytes2Array(Encrypted_FFT)

        self.IFFT_Array = ifft(FFT_Array)

        # Last we save results from IFFT to a .wav file


    def Array2Bytes(self,FFT_Array):
        print("Array 2 bytes")

    def Bytes2Array(self,FFT_Bytes):
        print("Bytes 2 array")






