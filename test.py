from AES.aes import AES_Cipher
from Blowfish.blowfish import BLOWFISH_Cipher

from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish

from Interpreters.Encrypt import Encrypt
from Interpreters.Decrypt import Decrypt

def test_blowfish(data):
       print("\n ----- BLOWFISH ----- \n")
       MODE = Blowfish.MODE_ECB
       test = BLOWFISH_Cipher()

       test.Encrypt(MODE, data)
       data_encriptada = test.get_cipher_data()
       print("Data encriptada: \n", data_encriptada)

       key = test.get_key()
       mode = test.get_mode()

       test2 = BLOWFISH_Cipher()
       test2.Decrypt(key, mode, data_encriptada)
       plain_data = test2.get_plain_data()
       print("Data desencriptada: \n",plain_data)

def test_aes(data):
       print("\n ----- AES ----- \n")
       test = AES_Cipher()

       test.Encrypt(AES.MODE_ECB, data)
       data_encriptada = test.get_cipher_data()
       print("Data encriptada: \n", data_encriptada)

       key = test.get_key()
       mode = test.get_mode()

       test2 = AES_Cipher()
       test2.Decrypt(key, mode, data_encriptada)
       plain_data = test2.get_plain_data()
       print("Data desencriptada: \n",plain_data)

def test_encrypt_signal():
       path = "Raw_Wavs/Flauta-LA.wav"
       Encriptacion = Encrypt()
       Encriptacion.encrypt_wav(path, "AES","cbc","MensajeEncriptado")

       ifftencry = Encriptacion.get_IFFTArray()

       key = Encriptacion.get_key()   # KEy en bytes b'-\x14\xdc]\xa3|\xf6\x9d\xfe\xc2\x16rW\xb6\xbe\xe5'
       print("\n KEY \n",key)
       keystr = key.decode('latin-1')
       Cipheriv = Encriptacion.get_CipherIV()

       Decriptacion = Decrypt()

       # Si o si necesitamos maxima amplitud de la señal original pre-encrypt para IFFT
       #Decriptacion.set_Max2Norm(Encriptacion.get_max2norm())

       # Si o si necesitamos tamaño para IFFTDecrypt
       #Decriptacion.set_TamañoSignalOriginal(tamaño)

       # Hardocdeo FFTa
       Decriptacion.set_FFTa(Encriptacion.get_FFTa())

       #Hardocdeo IFFT
       Decriptacion.set_IFFTEncrypt(ifftencry)

       # modos
       # "ecb" --> Electronic Code Book
       # "cbc" --> Cipher-Block Chaining

       Decriptacion.decrypt_wav("MensajeEncriptado","BLOB",keystr,"ebc")




def main():
       data = b"2+0i" \
              b"1.68992+1.38688i" \
              b"0.469455+2.36011i" \
              b"-0.878551+1.64365i" \
              b"0.136491+-0.0565362i" \
              b"3.47325+1.0536i" \
              b"4.17348+6.24606i" \
              b"-0.955416+9.7005" \
              b"-5.56233+5.56233i" \
              b"0.246421+-0.0242704i" \
              b"13.2134+8.82889i" \
              b"11.8181+38.9591i" \
              b"-34.5929+83.5147i" \
              b"3.47325+1.0536i" \
              b"4.17348+6.24606i" \
              b"-0.955416+9.7005" \
              b"-5.56233+5.56233i" \
              b"0.246421+-0.0242704i" \
              b"13.2134+8.82889i" \
              b"11.8181+38.9591i" \
              b"-34.5929+83.5147i" \
              b"3.47325+1.0536i" \
              b"4.17348+6.24606i" \
              b"-0.955416+9.7005" \
              b"-5.56233+5.56233i" \
              b"0.246421+-0.0242704i" \
              b"13.2134+8.82889i" \
              b"11.8181+38.9591i" \
              b"-34.5929+83.5147i" \
              b"172.209+-92.0479i"
       #test_aes(data)
       #test_blowfish(data)
       test_encrypt_signal()




if __name__=="__main__":
       main()
