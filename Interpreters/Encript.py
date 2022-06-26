import Interpreter

##################################
#           ENCRYPT              #
##################################
# Funciones:
#   FFT_to_byte --> Parsea de matriz FFT a string de bytes, agregando el signo entre cada numero
#   Encrypt_to_FFT_ASCII --> Parsea de encriptado (bytes) a ascii y con ese ascii armo un array FFT

class Encrypt(Interpreter):
    def __init__(self):
        self.time_samples = None


    def FFT_to_byte(self):
        string = ""
        for fil in range(len(self.FFT_Array[:][0])):
            for col in range(len(self.FFT_Array[0])):
                print("fila:", fil, "Col:", col)
                if (self.FFT_Array[fil][col] >= 0):
                    string = string + "+" + str(self.FFT_Array[fil][col])
                else:
                    string = string + "-" + str(-self.FFT_Array[fil][col])
        arr2 = bytes(string, 'ascii')
        return arr2

