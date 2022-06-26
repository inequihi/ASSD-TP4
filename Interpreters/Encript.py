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
