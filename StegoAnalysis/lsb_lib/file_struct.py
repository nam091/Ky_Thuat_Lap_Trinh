import os
import binascii
from PIL import Image
from PIL.ExifTags import TAGS

def read_exif_data(file_path):
    exif = {}
    try:
        with Image.open(file_path) as img:
            # Lấy thông tin exif từ ảnh
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    # Xử lý dữ liệu dạng bytes
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8', 'ignore')
                        except:
                            value = str(value)
                    exif[tag_name] = value
    except Exception as e:
        exif['Error'] = str(e)
    
    return exif

def ftypes(file_path):
    
    result = {
        'file_type': 'Unknown',
        'file size': os.path.getsize(file_path),
        'image_size': None,
        'extension': os.path.splitext(file_path)[1].lower(),
        'suspicious': False,
        'details': []
    }
    
    try:
        # Read file header and full content
        with open(file_path, 'rb') as f:
            with Image.open(file_path) as img:
                result['image_size'] = img.size
            header = f.read(16) # Đọc 16 byte đầu tiên của file
            hex_header = binascii.hexlify(header).decode('ascii') # Chuyển 16 byte đầu tiên sang hex
            f.seek(0) # Trở về đầu file
            content = f.read() # Đọc toàn bộ file
            hex_content = binascii.hexlify(content).decode('ascii') # Chuyển toàn bộ file sang hex
        
        # Identify file type based on magic numbers/signatures
        if hex_header.startswith('ffd8ff'): # Lấy 16 byte đầu tiên của file, nếu bắt đầu bằng ffd8ff thì file là ảnh
            result['file_type'] = 'JPEG'
            if result['extension'] not in ['.jpg', '.jpeg']: # Nếu phần mở rộng không phải là jpg hoặc jpeg thì file có thể là file ảnh nhưng không phải là file ảnh jpg
                result['suspicious'] = True
                result['details'].append(f"File có magic number JPEG nhưng có phần mở rộng {result['extension']}")
            
            # Check for data after JPEG EOF marker
            if 'ffd9' in hex_content:
                eof_pos = hex_content.rfind('ffd9') + 4
                if eof_pos < len(hex_content) - 2:
                    result['suspicious'] = True
                    result['details'].append("Dữ liệu ẩn được tìm thấy sau dấu EOF JPEG")
                
        elif hex_header.startswith('89504e47'):
            result['file_type'] = 'PNG'
            if result['extension'] != '.png':
                result['suspicious'] = True
                result['details'].append(f"File có magic number PNG nhưng có phần mở rộng {result['extension']}")
                
            # Check for data after PNG IEND chunk
            if '49454e44ae426082' in hex_content:
                eof_pos = hex_content.rfind('49454e44ae426082') + 16
                if eof_pos < len(hex_content) - 2:
                    result['suspicious'] = True
                    result['details'].append("Dữ liệu ẩn được tìm thấy sau dấu PNG IEND")
                
        elif hex_header.startswith('47494638'):
            result['file_type'] = 'GIF'
            if result['extension'] != '.gif':
                result['suspicious'] = True
                result['details'].append(f"File có magic number GIF nhưng có phần mở rộng {result['extension']}")
                
        elif hex_header.startswith('424d'):
            result['file_type'] = 'BMP'
            if result['extension'] != '.bmp':
                result['suspicious'] = True
                result['details'].append(f"File có magic number BMP nhưng có phần mở rộng {result['extension']}")
        
        # PDF files
        elif hex_header.startswith('25504446'):
            result['file_type'] = 'PDF'
            if result['extension'] != '.pdf':
                result['suspicious'] = True
                result['details'].append(f"File có magic number PDF nhưng có phần mở rộng {result['extension']}")
        
        # ZIP/Office Document
        elif hex_header.startswith('504b0304'):
            if '776f72642f' in hex_content:  # 'word/' in content
                result['file_type'] = 'DOCX'
                if result['extension'] != '.docx':
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number DOCX nhưng có phần mở rộng {result['extension']}")
            elif '786c2f' in hex_content:  # 'xl/' in content
                result['file_type'] = 'XLSX'
                if result['extension'] != '.xlsx':
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number XLSX nhưng có phần mở rộng {result['extension']}")
            elif '7070742f' in hex_content:  # 'ppt/' in content
                result['file_type'] = 'PPTX'
                if result['extension'] != '.pptx':
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number PPTX nhưng có phần mở rộng {result['extension']}")
            else:
                result['file_type'] = 'ZIP'
                if result['extension'] != '.zip':
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number ZIP nhưng có phần mở rộng {result['extension']}")
        
        # MP3 files
        elif hex_header.startswith('494433') or hex_header.startswith('fffb'):
            result['file_type'] = 'MP3'
            if result['extension'] != '.mp3':
                result['suspicious'] = True
                result['details'].append(f"File có magic number MP3 nhưng có phần mở rộng {result['extension']}")
        
        # MP4 files
        elif '66747970' in binascii.hexlify(header[4:12]).decode('ascii'):  # 'ftyp' in header
            result['file_type'] = 'MP4'
            if result['extension'] != '.mp4':
                result['suspicious'] = True
                result['details'].append(f"File có magic number MP4 nhưng có phần mở rộng {result['extension']}")
        
        # MS Office legacy document
        elif hex_header.startswith('d0cf11e0'):
            result['file_type'] = 'MS Office document'
            if result['extension'] not in ['.doc', '.xls', '.ppt']:
                result['suspicious'] = True
                result['details'].append(f"File có magic number MS Office document nhưng có phần mở rộng {result['extension']}")
        
        # RAR archives
        elif hex_header.startswith('526172211a07'):
            result['file_type'] = 'RAR'
            if result['extension'] != '.rar':
                result['suspicious'] = True
                result['details'].append(f"File có magic number RAR nhưng có phần mở rộng {result['extension']}")
        
        # 7z archives
        elif hex_header.startswith('377abcaf271c'):
            result['file_type'] = '7Z'
            if result['extension'] != '.7z':
                result['suspicious'] = True
                result['details'].append(f"File có magic number 7Z nhưng có phần mở rộng {result['extension']}")
        
        # GZIP files
        elif hex_header.startswith('1f8b08'):
            result['file_type'] = 'GZIP'
            if result['extension'] != '.gz':
                result['suspicious'] = True
                result['details'].append(f"File có magic number GZIP nhưng có phần mở rộng {result['extension']}")
        
        # BZIP2 files
        elif hex_header.startswith('425a68'):
            result['file_type'] = 'BZIP2'
            if result['extension'] != '.bz2':
                result['suspicious'] = True
                result['details'].append(f"File có magic number BZIP2 nhưng có phần mở rộng {result['extension']}")
        
        # XZ files
        elif hex_header.startswith('fd377a585a00'):
            result['file_type'] = 'XZ'
            if result['extension'] != '.xz':
                result['suspicious'] = True
                result['details'].append(f"File có magic number XZ nhưng có phần mở rộng {result['extension']}")
                
        # RTF files
        elif hex_header.startswith('7b5c727466'):  # {\\rtf
            result['file_type'] = 'RTF'
            if result['extension'] != '.rtf':
                result['suspicious'] = True
                result['details'].append(f"File có magic number RTF nhưng có phần mở rộng {result['extension']}")
        
        # Check for plaintext files
        elif all(32 <= int(hex_content[i:i+2], 16) <= 126 or int(hex_content[i:i+2], 16) in (9, 10, 13) 
                for i in range(0, min(32, len(hex_content)), 2)):
            
            # XML files
            if hex_header.startswith('3c3f786d6c') or b'<?xml' in header:  # <?xml
                result['file_type'] = 'XML'
                if result['extension'] != '.xml':
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number XML nhưng có phần mở rộng {result['extension']}")
            
            # HTML files
            elif b'<html' in header.lower() or b'<!doctype html' in header.lower():
                result['file_type'] = 'HTML'
                if result['extension'] not in ['.html', '.htm']:
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number HTML nhưng có phần mở rộng {result['extension']}")
            
            # JSON files
            elif header.startswith(b'{"') or header.startswith(b'['):
                result['file_type'] = 'JSON'
                if result['extension'] != '.json':
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number JSON nhưng có phần mở rộng {result['extension']}")
            
            # Plain text
            else:
                result['file_type'] = 'Text'
                if result['extension'] not in ['.txt', '.csv', '.log', '.md']:
                    result['suspicious'] = True
                    result['details'].append(f"File có magic number dạng văn bản nhưng có phần mở rộng {result['extension']}")
                    
    except Exception as e:
        result['suspicious'] = True
        result['details'].append(f"Lỗi xác định kiểu file: {str(e)}")
    
    return result