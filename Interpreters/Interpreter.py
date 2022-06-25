#############################################
#               INTERPRETER                 #
#############################################

# Interpreter es una clase madre, de la cual heredan las clases Encrypy y Decrypt.
# Notamos que ambos procesos utilizan funciones similares tales como:
#       Leer archivo de audio original (read_wav)
#       Aplicar transformacion FFT (FFT)
#       Aplicar algoritmo de encripcion
#       Aplicar transformacion inversa IFFT
#       Guardar archivo de audio encriptado .wav

class Interpreter:
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
