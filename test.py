import pandas as pd
from AES.aes import AES_Cipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from base64 import b64encode
from base64 import b64decode

from Crypto.Util.Padding import pad, unpad

test = AES_Cipher()
key = get_random_bytes(16)
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
       b"172.209+-92.0479i"

test.Encrypt(key, AES.MODE_ECB, data)
data_encriptada = test.get_cipher_data()
print("Data encriptada: \n",data_encriptada)

#test.Decrypt(key, data_encriptada, AES.MODE_ECB)
#plain_data = test.get_plain_data()
#print(plain_data)