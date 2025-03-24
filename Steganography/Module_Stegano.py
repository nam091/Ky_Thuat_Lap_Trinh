import os
from pickletools import optimize
import sys
from time import time
from PIL import Image
from numpy import size
from Crypt import AESCipher
import struct
from check_file_type import file_type as ftype


def Image_Steganography(action: int, input_image_path: str, output_path: str, secret_file_path: str, lsb_bits: int, compress_level: int, password: str):
    """
    Main function for steganography operations.
    
    Args:
        input_image_path: Địa chỉ ảnh gốc
        output_path: Địa chỉ ảnh kết quả
        secret_file_path: Địa chỉ file bí mật để ẩn
        lsb_bits: Số bit ít quan trọng để sử dụng
        action: 0: Analys, 1: Encode, 2: Decode
        compress_level: Mức Nén ảnh PNG
        password: Mật khẩu để mã hóa dữ liệu
    """
    
    
    # Decompose a binary file into an array of bits
    def decompose(data):
        v = []
        fSize = len(data)  # Kích thước payload
        bytes_data = [b for b in struct.pack("i", fSize)] # Thêm kích thước payload vào đầu dữ liệu
        bytes_data += [b for b in data]  # Thêm dữ liệu vào sau kích thước payload
        for b in bytes_data:
            for i in range(7, -1, -1): # Lấy từ bit cao nhất đến bit thấp nhất
                v.append((b >> i) & 0x1) # Lấy bit thứ i của byte b và thêm vào mảng v
        return v # Trả về mảng bit (0, 1) của payload

    # Assemble an array of bits into a binary file
    def assemble(v):
        bytes_data = bytearray() # Khởi tạo mảng bytes_data rỗng
        length = len(v)
        for idx in range(0, len(v) // 8): # Duyệt qua từng byte (8 bit) của mảng v
            byte = 0
            for i in range(0, 8): # Duyệt qua từng bit trong byte
                if (idx * 8 + i < length): # Duyệt đến khi hết mảng v
                    byte = (byte << 1) + v[idx * 8 + i] # Thêm bit thứ i vào byte
            bytes_data.append(byte) # Ghi byte vào mảng bytes_data
        payload_size = struct.unpack("i", bytes_data[:4])[0] # Đọc kích thước payload từ 4 byte đầu
        return bytes_data[4: payload_size + 4] # Trả về dữ liệu từ byte thứ 4 đến byte thứ 4 + kích thước payload

    # Set the i-th bit of v to x
    def set_bit(n, i, x):
        mask = 1 << i # Tạo mask với bit thứ i bằng 1, các bit khác bằng 0
        n &= ~mask # Đặt bit thứ i của n bằng 0
        if x:  # Nếu x = 1
            n |= mask # Đặt bit thứ i của n bằng 1
        return n # Trả về giá trị n mới

    def Embed(imgFile, output_path, payload, compress_level, password):
        print("[+] Bắt đầu nhúng Payload vào ảnh...")
        if not output_path:
            base = os.path.splitext(imgFile)[0]
            ext = os.path.splitext(imgFile)[1].lower()
            output_path = f"{base}_encoded{ext}"
        else:
            ext = os.path.splitext(output_path)[1].lower()
        
        img = Image.open(imgFile) # Mở ảnh
        original_format = img.format  # Lưu định dạng gốc
        if original_format not in ["PNG", "JPEG", "JPG"]:
            print("[-] Định dạng ảnh không hợp lệ. Chỉ hỗ trợ PNG và JPEG.")
            return
        (width, height) = img.size  # Lấy kích thước ảnh
        conv = img.convert("RGBA")
        print(f"[*] Kích thước ảnh: {width}x{height} pixels.")
        size_of_img = os.path.getsize(imgFile)  # Lấy kích thước ảnh gốc
        print(f"[+] Kích thước file gốc: {size_of_img:.1f} bytes")
        if ext == ".jpg":
            channels = 3 # JPEG chỉ có 3 kênh màu RGB
        elif ext == ".png":
            channels = 4
        max_bits_img = width * height * lsb_bits * channels
        print(f"[*] Tổng LSB của ảnh: {max_bits_img} bits.")
        
        if os.path.isfile(payload):
            with open(payload, "rb") as f:
                data = f.read() # Đọc dữ liệu từ file ở dạng bytes
        elif isinstance(payload, str):
            data = payload.encode('utf-8')  # Chuỗi text, chuyển thành bytes
        elif isinstance(payload, bytes):
            data = payload  # Đã là bytes, không cần xử lý
        else:
            raise ValueError("[-] Payload không hợp lệ, cần là đường dẫn file, chuỗi text hoặc bytes")
        size_of_payload = len(data)  # Lấy kích thước payload
        print(f"[+] Kích thước của Payload: {size_of_payload:.1f} Bytes ")

        if password:
            cipher = AESCipher(password)
            data_enc = cipher.encrypt_data(data)
        else:
            data_enc = data
        v = decompose(data_enc)

        while(len(v) % 3):
            v.append(0)

        payload_size = len(v)
        print("[+] Tổng số lượng bit của Payload: %.1f bits " % (payload_size))
        if (payload_size > max_bits_img):
            print("[-] Không thể nhúng. Tệp quá lớn")
            sys.exit()
        
        steg_img = Image.new("RGBA", (width, height)) # Tạo ảnh mới với kích thước và chế độ màu RGBA giống ảnh gốc
    
        idx = 0
        for h in range(height):
            for w in range(width):
                r, g, b, a = conv.getpixel((w, h)) # Lấy giá trị màu tại vị trí (w, h)
                
                for bit in range(lsb_bits): # Duyệt qua số bit với lsb_bits có thể tùy chỉnh
                    
                    if idx < len(v):
                        r = set_bit(r, bit, v[idx]) # Thay đổi bit thứ bit của kênh màu red
                        g = set_bit(g, bit, v[idx + 1]) # Thay đổi bit thứ bit của kênh màu green
                        b = set_bit(b, bit, v[idx + 2]) # Thay đổi bit thứ bit của kênh màu blue
                    steg_img.putpixel((w, h), (r, g, b, a)) # Đặt giá trị màu mới vào ảnh
                    idx += 3 # Tăng chỉ số lên 3 để xử lý 3 kênh màu tiếp theo
            
        if ext in [".jpg", ".jpeg"]:
            steg_img = steg_img.convert("RGB")  # Chuyển đổi ảnh sang định dạng RGB
            quality = 100 - min(compress_level * 10, 95)
            steg_img.save(output_path, format="JPEG", quality=quality)
        elif ext == ".png":
            if compress_level < 0 or compress_level > 9:
                compress_level = 0
            steg_img.save(output_path, optimize=True, format="PNG", compress_level=compress_level)
        else:
            steg_img.save(output_path, optimize=True, format=original_format)
        size_of_steg_img = os.path.getsize(output_path)  # Lấy kích thước ảnh đã nhúng
        print(f"[+] Dung lượng ảnh đã lưu: {size_of_steg_img:.1f} Bytes")
        
        if password:
            print(f"[+] {payload} đã nhúng thành công với mật khẩu {password}!")
        else:
            print(f"[+] {payload} đã nhúng thành công!")
        print(f"[+] Đã lưu tại địa chỉ {output_path}")
        print("=" * 50)
        print("So sánh kích thước ảnh gốc và ảnh đã nhúng:")
        print(f"[+] Kích thước ảnh gốc: {size_of_img:.1f} Bytes")
        print(f"[+] Kích thước ảnh đã nhúng: {size_of_steg_img:.1f} Bytes")
        print("-" * 50)
        print(f"[+] Kích thước lệch:    {size_of_steg_img - size_of_img:.1f} Bytes")
        print(f"[+] Kích thước payload: {size_of_payload:.1f} Bytes")
        


    def Recover(in_file, out_file, password):
    	# Process source image
        print("[+] Bắt đầu khôi phục ảnh...")
        img = Image.open(in_file)
        (width, height) = img.size
        conv = img.convert("RGBA")
        print("[+] Kích thước ảnh: %dx%d pixels." % (width, height))

        bits = [] # Mảng chứa bit của ảnh
        for h in range(height):
            for w in range(width):
                (r, g, b, a) = conv.getpixel((w, h))
                for bit in range(lsb_bits):
                    bits.append((r >> bit) & 1) # Ghi số bit cuối của kênh màu red vào mảng bits
                    bits.append((g >> bit) & 1) # Ghi số bit cuối của kênh màu green vào mảng bits
                    bits.append((b >> bit) & 1) # Ghi số bit cuối của kênh màu blue vào mảng bits
        data_out = bytes(assemble(bits))        # Gom các bit thành dữ liệu và chuyển thành bytes

        if password:
            cipher = AESCipher(password)
            data_dec = cipher.decrypt_data(data_out)
            # Ensure data_dec is bytes, not string
            if isinstance(data_dec, str):
                data_dec = data_dec.encode('utf-8')
        else:
            data_dec = data_out

        if not out_file:
            out_file = os.path.dirname(in_file) + "/" + os.path.basename(in_file).split(".")[0]

        with open(out_file, "wb") as out_f: # Ghi dữ liệu đã giải mã vào file
            out_f.write(data_dec) # Ghi dữ liệu đã giải mã vào file
        ftype(out_file, password) # Kiểm tra loại file và giải nén nếu cần
        
        if password:
            print(f"[+] File đã khôi phục thành công với mật khẩu {password}!")

    print("=" * 50)
    begin = time()
    match action:
        case 0:
            Embed(input_image_path, output_path, secret_file_path, compress_level, password)
        case 1:
            Recover(input_image_path, output_path, password)
        case _:
            raise ValueError("[-] Lỗi với các đối số.")
    print(f"[+] Thời gian thực thi: {time() - begin:.2f}s")
    print("=" * 50)