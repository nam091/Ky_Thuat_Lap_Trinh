import os
import argparse
from Module_StegaAnalysis import compare_images, analyse
from lsb_lib.file_struct import ftypes

use_help = "python ./StegaAnalysis.py -h -----> help"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--Compare', action='store_true', help="Để so sánh giữa ảnh gốc và ảnh đã ẩn")
    parser.add_argument('-A', '--Analysis', action='store_true', help="Phân tích mức độ entropy của lsb trong ảnh")
    parser.add_argument('-Fs', '--Struct_File', action='store_true', help="Kiểm tra cấu trúc file")
    parser.add_argument('-org', '--original', help="Đường dẫn tới file gốc")
    parser.add_argument('-mod', '--modified', help="Đường dẫn tới file đã bị chỉnh sửa")
    parser.add_argument('-o', '--output_path', help="Đường dẫn đến thư mục lưu trữ -- default = Image_Output/", default='./Image_Output')

    args = parser.parse_args()
    
    original_image_path = args.original
    modified_image_path = args.modified
    output_path = args.output_path
    
    
    def check_path(path):
        if not os.path.exists(path) or not os.path.isfile(path):
            raise ValueError("[-] Đường dẫn file gốc không hợp lệ")

    if args.Compare:
        check_path(original_image_path)
        check_path(modified_image_path)
        for color in ['RGB', 'delta']:
            match_percentage = compare_images(original_image_path, modified_image_path, color,output_path)
            print(f"[+] Độ tương đồng giữa hai ảnh với màu {color}: {match_percentage:.2f}%")
    elif args.Struct_File:
        check_path(modified_image_path)
        file_info = ftypes(modified_image_path)
        print(f"[+] Kiểu file: {file_info['file_type']}")
        print(f"[+] Phần mở rộng: {file_info['extension']}")
        if file_info['suspicious']:
            print(f"[-] File có vẻ bất thường")
            print("\n".join(file_info['details']))
    elif args.Analysis:
        plot_path, _ = analyse(original_image_path, modified_image_path)
        print(f"[+] Biểu đồ được lưu tại: {plot_path}")
    else:
        raise ValueError("[-] Cần chọn một hành động để thực hiện")

if __name__ == "__main__":
    main()