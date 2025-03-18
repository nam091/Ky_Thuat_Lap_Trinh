import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import sys

class AESCipher:

    def __init__(self, key): 
        self.bs = 32  # kích thước khối
        self.key = hashlib.sha256(key.encode()).digest()  # băm khóa thành 32 bytes

    def encrypt_data(self, raw):
        raw_bytes = raw if isinstance(raw, bytes) else raw.encode() # Chuyển dữ liệu thành bytes
        raw_bytes = self._pad(raw_bytes) # Thêm padding cho dữ liệu để đủ kích thước khối
        iv = Random.new().read(AES.block_size) # Tạo vector khởi tạo ngẫu nhiên
        cipher = AES.new(self.key, AES.MODE_CBC, iv) # Tạo bản mã với khóa và iv
        return iv + cipher.encrypt(raw_bytes) # Trả về dữ liệu đã mã hóa kèm iv dưới dạng bytes

    def decrypt_data(self, enc):
        try:
            iv = enc[:AES.block_size] # Lấy iv từ dữ liệu mã hóa
            cipher = AES.new(self.key, AES.MODE_CBC, iv) # Tạo bản giải mã với khóa và iv
            decrypted = self._unpad(cipher.decrypt(enc[AES.block_size:])) # Giải mã dữ liệu và loại bỏ padding
            return decrypted # Trả về dữ liệu đã giải mã dưới dạng bytes
        except (ValueError, KeyError) as e:
            print(f"Sai Mật khẩu hoặc dữ liệu bị hỏng:\n{str(e)}")
            sys.exit(1)

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * bytes([self.bs - len(s) % self.bs])

    @staticmethod
    def _unpad(s):
        return s[:-s[-1]]
