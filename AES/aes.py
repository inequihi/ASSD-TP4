from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode
from base64 import b64decode
from Crypto.Random import get_random_bytes

class AES_Cipher:
    def __init__(self):
        self.plain_data = None
        self.cipher_data = None
        self.IV_cipher = None  # Information available to each party of the communication in order to determine the IV
        self.status = 0  # Status of object AES_Cipher:
        self.Key = None
        self.Mode = None

        # 0 - Data NOT available
        # 1 - Encryption data available
        # 2 - Decrypted data available

        #   MODE_ECB: Electronic Code Book
        #             Chaining mode. This is the simplest encryption mode.
        #             Each of the plaintext blocks is directly encrypted into a ciphertext block,
        #             independently of any other block.
        #             This mode exposes frequency of symbols in your plaintext.
        #             Other modes (e.g. CBC) should be used instead.
        #             Total number of bits in the plaintext must be a multiple of the block size b.
        #             Disadvantage: Identical plaintext blocks will result in identical ciphertext,
        #                           therefore an attacker can identify repetition.
        #   MODE_CBC: Cipher-Block Chaining
        #             Introduces a vector that alters the first plaintext block before it is encrypted.
        #             Each of the ciphertext blocks depends on the current and all previous plaintext blocks.
        #             An Initialization Vector (IV) is required.
        #             The IV is a data block to be transmitted to the receiver.
        #             The IV can be made public, but it must be authenticated by the receiver
        #             and it should be picked randomly.

    def Encrypt(self, MODE, plain_data):
        # The cipher objects are destroyed once the data is encrypted. The receiver only gets cipher_data and iv
        self.GenerateKey()
        self.Mode = MODE
        cipher_object = AES.new(self.Key, MODE)

        if MODE == AES.MODE_CBC:
            # An IV must be generated for each execution of the encryption operation, and the same
            # IV is necessary for the corresponding execution of the decryption operation. Therefore, the IV, or
            # information that is sufficient to calculate the IV, must be available to each party to the communication.
            # We will use the random IV value generated by the library and apply the forward cipher function,
            # under the same key that is used for the encryption of the plain_data.
            self.IV_cipher = b64encode(cipher_object.iv).decode('utf-8')

        self.cipher_data = cipher_object.encrypt(pad(plain_data, AES.block_size))
        self.status = 1

    def Decrypt(self, KEY, MODE, cipher_data, cipher_IV=None):
        # We create new cipher objects for decryption
        if MODE == AES.MODE_ECB:
            cipher_object = AES.new(KEY, MODE)

        elif MODE == AES.MODE_CBC:
            cipher_object = AES.new(KEY, MODE, b64decode(cipher_IV))

        self.plain_data = unpad(cipher_object.decrypt(cipher_data), AES.block_size)
        self.status = 2

    def GenerateKey(self):
        # We generate the private key which we will use to encrypt the data and the public key that
        # will be used by recipient to decrypt the data.
        self.Key = get_random_bytes(16)

    # GETTERS
    def get_cipher_data(self):
        if self.status == 1:
            return self.cipher_data
        else:
            return None

    def get_cipher_IV(self):
        if self.status == 1:
            return self.IV_cipher
        else:
            return None

    def get_plain_data(self):
        if self.status == 2:
            return self.plain_data
        else:
            return None

    def get_key(self):
        return self.Key

    def get_mode(self):
        return self.Mode