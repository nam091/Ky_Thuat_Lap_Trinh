import os

def file_type(out_file, password):
    with open(out_file, "rb") as f:
            header = f.read(16)  # Read first 16 bytes for signature detection

            file_type = None
            renamed_file = out_file
            out_name = os.path.dirname(out_file) + "/" + os.path.basename(out_file).split(".")[0]
            # Check for common file signatures
            if header.startswith(b'\x89PNG\r\n\x1a\n'):
                file_type = "PNG"
                renamed_file = out_name + ".png"
            elif header.startswith(b'\xff\xd8\xff'):
                file_type = "JPEG"
                renamed_file = out_name + ".jpg"
            elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
                file_type = "GIF"
                renamed_file = out_name + ".gif"
            elif header.startswith(b'%PDF'):
                file_type = "PDF"
                renamed_file = out_name + ".pdf"
            elif header.startswith(b'PK\x03\x04'):
                file_type = "ZIP/Office Document"
                renamed_file = out_name + ".zip"
            elif header.startswith(b'ID3') or header.startswith(b'\xff\xfb'):
                file_type = "MP3"
                renamed_file = out_name + ".mp3"
            elif b'ftyp' in header[4:12]:
                file_type = "MP4"
                renamed_file = out_name + ".mp4"
            elif header.startswith(b'\xd0\xcf\x11\xe0'):
                file_type = "MS Office document"
                renamed_file = out_name + ".doc"
            elif all(32 <= b <= 126 or b in (9, 10, 13) for b in header if b):
                file_type = "Text"
                renamed_file = out_name + ".txt"
            elif header.startswith(b'Rar!\x1A\x07'):
                file_type = "RAR"
                renamed_file = out_name + ".rar"
            elif header.startswith(b'7z\xBC\xAF\x27\x1C'):
                file_type = "7Z"
                renamed_file = out_name + ".7z"
            elif header.startswith(b'\x1F\x8B\x08'):
                file_type = "GZIP"
                renamed_file = out_name + ".gz"
            elif header.startswith(b'BZh'):
                file_type = "BZIP2"
                renamed_file = out_name + ".bz2"
            elif header.startswith(b'\xFD\x37\x7A\x58\x5A\x00'):
                file_type = "XZ"
                renamed_file = out_name + ".xz"
            elif header[0:4] == b'\x50\x4B\x03\x04' and b'word/' in header:
                file_type = "DOCX"
                renamed_file = out_name + ".docx"
            elif header[0:4] == b'\x50\x4B\x03\x04' and b'xl/' in header:
                file_type = "XLSX"
                renamed_file = out_name + ".xlsx"
            elif header[0:4] == b'\x50\x4B\x03\x04' and b'ppt/' in header:
                file_type = "PPTX"
                renamed_file = out_name + ".pptx"
            elif header.startswith(b'{\\rtf'):
                file_type = "RTF"
                renamed_file = out_name + ".rtf"
            elif header.startswith(b'<?xml') or b'<?xml' in header:
                file_type = "XML"
                renamed_file = out_name + ".xml"
            elif b'<html' in header.lower() or b'<!doctype html' in header.lower():
                file_type = "HTML"
                renamed_file = out_name + ".html"
            elif header.startswith(b'{"') or header.startswith(b'['):
                file_type = "JSON"
                renamed_file = out_name + ".json"

            if file_type and renamed_file != out_file:
                os.rename(out_file, renamed_file)
                print(f"[+] Phát hiện loại file đúng: {file_type}")
                print(f"[+] Đã khôi phục lưu tại địa chỉ {renamed_file}")
            else:
                print("[-] Không thể xác định loại file hoặc file đã bị hỏng")