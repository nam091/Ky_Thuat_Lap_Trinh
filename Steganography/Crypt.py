import hashlib
import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AESCipher:

    def __init__(self, key): 
        self.bs = 32  # kích thước khối
        self.key = hashlib.sha256(key.encode()).digest()  # băm khóa thành 32 bytes

    def encrypt_data(self, raw):
        raw_bytes = raw if isinstance(raw, bytes) else raw.encode() # Chuyển dữ liệu thành bytes
        raw_bytes = self._pad(raw_bytes) # Thêm padding cho dữ liệu để đủ kích thước khối
        iv = os.urandom(16) # Tạo vector khởi tạo ngẫu nhiên
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(raw_bytes) + encryptor.finalize()
        return iv + encrypted_data # Trả về dữ liệu đã mã hóa kèm iv dưới dạng bytes

    def decrypt_data(self, enc):
        try:
            iv = enc[:16] # Lấy iv từ dữ liệu mã hóa
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted = decryptor.update(enc[16:]) + decryptor.finalize()
            decrypted = self._unpad(decrypted) # Giải mã dữ liệu và loại bỏ padding
            return decrypted # Trả về dữ liệu đã giải mã dưới dạng bytes
        except (ValueError, KeyError) as e:
            print(f"Sai Mật khẩu hoặc dữ liệu bị hỏng:\n{str(e)}")
            sys.exit(1)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * bytes([self.bs - len(s) % self.bs])

    @staticmethod
    def _unpad(s):
        padding_value = s[-1]
        if padding_value > 32:
            return s  # No padding or invalid padding
        return s[:-padding_value]
