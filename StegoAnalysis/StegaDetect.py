import os
import argparse
from Module_Stega import Image_Steganography as IMS

use_help = "python ./Steganography.py -h -----> help"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--Hide', action='store_true', help="Để ẩn dữ liệu trong ảnh")
    parser.add_argument('-R', '--Recover', action='store_true', help="Để khôi phục dữ liệu từ ảnh")
    parser.add_argument('-i', '--input', help="Đường dẫn tới file input")
    parser.add_argument('-o', '--output', help="Đường dẫn tới file output - Default: input_encoded.png")
    parser.add_argument('-s', '--secret', help="Đường dẫn tới file secret hoặc chuỗi tin nhắn", default=None)
    parser.add_argument('-n', '--number_of_bits', help="Số bits để chèn vào ảnh - Default: 1", default=1)
    parser.add_argument('-c', '--compression_level', help="Cấp độ nén ảnh PNG (0-9) - Default: 1", default=1)
    parser.add_argument('-p', '--password', help="Mật khẩu để mã hóa dữ liệu - Default: None", default=None)
    args = parser.parse_args()
    
    input_image_path = args.input
    output_image_path = args.output
    secret_file_path = args.secret
    lsb_bits = int(args.number_of_bits)
    compression = int(args.compression_level)
    password = args.password

    if not os.path.exists(input_image_path) or not os.path.isfile(input_image_path):
        raise ValueError("[-] Cần địa chỉ ảnh để thực hiện")
    
    if args.Hide:
        if not secret_file_path:
            raise ValueError("[-] Cần địa chỉ file bí mật để ẩn")
        action = 0
    elif args.Recover:
        action = 1
    else:
        raise ValueError("[-] Cần chọn một hành động: Hide hoặc Recover")
    
    IMS(action, input_image_path, output_image_path, secret_file_path, lsb_bits, compression, password)

if __name__ == "__main__":
    main()