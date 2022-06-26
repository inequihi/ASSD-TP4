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
        self.data_byte_enc = None  # b'%5yu/223?'
        self.data_matrix_FFT = None  # [ [1,2] [3,4] ]


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

    def Encrypt_to_FFT_ASCII(self, data):

        self.data_byte_enc = data
        str_data = self.data_byte_encripted.decode("latin-1")
        self.data_matrix_FFT = np.array([[0, 0]])
        for i in range(0, len(str_data), 2):
            word1 = str_data[i]
            word1_ASCII = ord(word1)
            word2 = str_data[i + 1]
            word2_ASCII = ord(word2)

            pre_answer = np.array([[int(word1_ASCII), int(word2_ASCII)]])
            if (i == 0):
                self.data_matrix_FFT = pre_answer
            else:
                self.data_matrix_FFT = np.append(self.data_matrix_FFT, pre_answer, axis=0)

