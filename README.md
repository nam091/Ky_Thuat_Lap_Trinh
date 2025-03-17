# KỸ THUẬT LẬP TRÌNH NHÓM 7
## NGHIÊN CỨU IMAGE FORENSICS

### HOW TO RUN CODE?
**Steganography**
```
Python Steganography.py [-h] [-a] [-H] [-R] [-i INPUT] [-o OUTPUT] [-s SECRET] [-n NUMBER_OF_BITS] [-c COMPRESSION_LEVEL] [-p PASSWORD]
```
options:*
```
-h, --help            show this help message and exit
-a, --analyze         Để phân tích ảnh
-H, --Hide            Để ẩn dữ liệu trong ảnh
-R, --Recover         Để khôi phục dữ liệu từ ảnh
-i INPUT, --input INPUT
                      Đường dẫn tới file input
-o OUTPUT, --output OUTPUT
                      Đường dẫn tới file output
-s SECRET, --secret SECRET
                      Đường dẫn tới file secret hoặc chuỗi tin nhắn
-n NUMBER_OF_BITS, --number_of_bits NUMBER_OF_BITS
                      Số bits để chèn vào ảnh
-c COMPRESSION_LEVEL, --compression_level COMPRESSION_LEVEL
                      Cấp độ nén ảnh PNG (0-9)
-p PASSWORD, --password PASSWORD
                      Mật khẩu để mã hóa dữ liệu
```
**StegaAnalysis**
```
Python StegaAnalysis.py [-h] [-C] [-A] [-Fs] [-org ORIGINAL] [-mod MODIFIED] [-o OUTPUT_PATH]
```
*Option*
```
-h, --help            show this help message and exit
-C, --Compare         Để so sánh giữa ảnh gốc và ảnh đã ẩn
-A, --Analysis        Phân tích mức độ entropy của lsb trong ảnh
-Fs, --Struct_File    Kiểm tra cấu trúc file
-org ORIGINAL, --original ORIGINAL
                      Đường dẫn tới file gốc
-mod MODIFIED, --modified MODIFIED
                      Đường dẫn tới file đã bị chỉnh sửa
-o OUTPUT_PATH, --output_path OUTPUT_PATH
                      Đường dẫn đến thư mục lưu trữ -- default = Image_Output/
```

### TÍNH NĂNG
**HIDE**
- Có thể nhúng các loại file: chuỗi, ảnh, văn bản, file nén

### KHÔNG THỂ CHẠY FILE?

*Lỗi thiếu thư viện*
- Để cài đặt: 
```
pip install -r requirement.txt
```
