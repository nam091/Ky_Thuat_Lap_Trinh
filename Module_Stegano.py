import os
import sys
from time import time
from PIL import Image
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
        fSize = len(data)
        bytes_data = [b for b in struct.pack("i", fSize)]
     
        bytes_data += [b for b in data] 
        for b in bytes_data:
            for i in range(7, -1, -1):
                v.append((b >> i) & 0x1)
        return v

    # Assemble an array of bits into a binary file
    def assemble(v):    
        bytes_data = bytearray()

        length = len(v)
        for idx in range(0, len(v) // 8):
            byte = 0
            for i in range(0, 8):
                if (idx*8+i < length):
                    byte = (byte << 1) + v[idx*8+i]
            bytes_data.append(byte)

        payload_size = struct.unpack("i", bytes_data[:4])[0]
        return bytes_data[4: payload_size + 4]

    # Set the i-th bit of v to x
    def set_bit(n, i, x):
        mask = 1 << i
        n &= ~mask
        if x:
            n |= mask
        return n

    # Embed payload file into LSB bits of an image
    def Embed(imgFile, payload, password):
    	# Process source image
        nonlocal output_path
        print("[+] Bắt đầu nhúng Payload vào ảnh...")
        img = Image.open(imgFile)
        (width, height) = img.size
        conv = img.convert("RGBA")
        print("[*] Kích thước ảnh: %dx%d pixels." % (width, height))
        max_size = width * height * 3.0 / 8 / 1024        # max payload size
        print("[*] Kích thước bits của ảnh: %.2f KB." % (max_size))

        with open(payload, "rb") as f:
            data = f.read()
        print("[+] Kích thước Payload: %.3f KB " % (len(data) / 1024.0))

        if password:
            cipher = AESCipher(password)
            data_enc = cipher.encrypt_data(data)
        else:
            data_enc = data

        # Process data from payload file
        v = decompose(data_enc)

        # Add until multiple of 3
        while(len(v) % 3):
            v.append(0)

        payload_size = len(v) / 8 / 1024.0
        print("[+] Kích thước bits của Payload: %.3f KB " % (payload_size))
        if (payload_size > max_size - 4):
            print("[-] Không thể nhúng. Tệp quá lớn")
            sys.exit()
        # Create output image
        steg_img = Image.new('RGBA',(width, height))
        
    
        idx = 0
        for h in range(height):
            for w in range(width):
                r, g, b, a = conv.getpixel((w, h))
                
                # Process each channel
                for bit in range(lsb_bits):
                    # For red channel
                    if idx < len(v):
                        r = set_bit(r, bit, v[idx])
                        g = set_bit(g, bit, v[idx + 1])
                        b = set_bit(b, bit, v[idx + 2])
                    steg_img.putpixel((w, h), (r, g, b, a))
                    idx += 3
            
            
        if not output_path:
            output_path = os.path.dirname(input_image_path) + "/" + os.path.basename(input_image_path).split(".")[0] + "_encoded.png"
            
        exif_data = img.getexif()
        steg_img.save(output_path, exif=exif_data, compress_level=compress_level)
        if password:
            print(f"[+] {payload} đã nhúng thành công với mật khẩu {password}!")
        print(f"[+] Đã lưu tại địa chỉ {output_path}")


    def Recover(in_file, out_file, password):
    	# Process source image
        print("[+] Bắt đầu khôi phục ảnh...")
        img = Image.open(in_file)
        (width, height) = img.size
        conv = img.convert("RGBA")
        print("[+] Kích thước ảnh: %dx%d pixels." % (width, height))

        v = []
        for h in range(height):
            for w in range(width):
                (r, g, b, a) = conv.getpixel((w, h))
                for bit in range(lsb_bits):
                    v.append((r >> bit) & 1)
                    v.append((g >> bit) & 1)
                    v.append((b >> bit) & 1)

        data_out = bytes(assemble(v))

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

        with open(out_file, "wb") as out_f:
            out_f.write(data_dec)
        ftype(out_file, password)
        if password:
            print(f"[+] File đã khôi phục thành công với mật khẩu {password}!")

    print("=" * 50)
    begin = time()
    match action:
        case 0:
            Embed(input_image_path, secret_file_path, password)
        case 1:
            Recover(input_image_path, output_path, password)
        case _:
            raise ValueError("[-] Lỗi với các đối số.")
    print(f"[+] Thời gian thực thi: {time() - begin:.2f}s")
    print("=" * 50)