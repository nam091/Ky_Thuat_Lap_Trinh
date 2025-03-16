import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import sys

class AESCipher:

    def __init__(self, key): 
        self.bs = 32  # Block size
        self.key = hashlib.sha256(key.encode()).digest()  # 32 bit digest

    def encrypt_data(self, raw):
        raw_bytes = raw if isinstance(raw, bytes) else raw.encode()
        raw_bytes = self._pad(raw_bytes)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw_bytes)

    def decrypt_data(self, enc):
        try:
            iv = enc[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted = self._unpad(cipher.decrypt(enc[AES.block_size:]))
            # Return as binary data without decoding
            return decrypted
        except (ValueError, KeyError) as e:
            print(f"Sai Mật khẩu hoặc dữ liệu bị hỏng:\n{str(e)}")
            sys.exit(1)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * bytes([self.bs - len(s) % self.bs])

    @staticmethod
    def _unpad(s):
        return s[:-s[-1]]
