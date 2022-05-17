from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class RSAESOAEP_Cipher:
    def __init__(self):
        self.plain_data = None
        self.cipher_data = None
        self.status = 0
        self.public_key = None
        self.private_key = None
        self.session_key = None
        self.encrypted_session_key = None

    def Encrypt(self,plain_data):
        self.GenerateKey()
        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(self.public_key)
        self.encrypted_session_key = cipher_rsa.encrypt(self.session_key)

        # Encrypt data with AES session key
        cipher_object = AES.new(self.session_key, AES.MODE_EAX)
        self.cipher_data = cipher_object.encrypt(pad(plain_data, AES.block_size))
        self.status = 1

    def Decrypt(self, privKEY, encsesKEY, cipher_data):
        # Recipient receives private RSA key and encripted session key
        # Decrypt the session key with private RSA key
        cipher_rsa = PKCS1_OAEP.new(privKEY)
        session_key = cipher_rsa.decrypt(encsesKEY)

        # Decrypt the data with AES session key
        cipher_object = AES.new(session_key, AES.MODE_EAX)
        self.plain_data = unpad(cipher_object.decrypt(cipher_data), AES.block_size)
        self.status = 2

    def GenerateKey(self):
        # We generate the private key which we will use to encrypt the data and the public key that
        # will be used by recipient to decrypt the data.
        self.session_key = get_random_bytes(16)
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.public_key()


    # GETTERS
    def get_private_key(self):
        return self.private_key

    def get_encrypted_session_key(self):
        return self.encrypted_session_key

    def get_plain_data(self):
        if self.status == 2:
            return self.plain_data
        else:
            return None

    def get_cipher_data(self):
        if self.status == 1:
            return self.cipher_data
        else:
            return None
