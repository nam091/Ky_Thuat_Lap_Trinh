import os
import binascii

def ftypes(file_path):
    
    result = {
        'file_type': 'Unknown',
        'extension': os.path.splitext(file_path)[1].lower(),
        'suspicious': False,
        'details': []
    }
    
    try:
        # Read file header and full content
        with open(file_path, 'rb') as f:
            header = f.read(16)
            hex_header = binascii.hexlify(header).decode('ascii')
            
            # Return to beginning and read full content for EOF analysis
            f.seek(0)
            content = f.read()
            hex_content = binascii.hexlify(content).decode('ascii')
        
        # Identify file type based on magic numbers/signatures
        if hex_header.startswith('ffd8ff'):
            result['file_type'] = 'JPEG'
            if result['extension'] not in ['.jpg', '.jpeg']:
                result['suspicious'] = True
                result['details'].append(f"File signature is JPEG but has {result['extension']} extension")
            
            # Check for data after JPEG EOF marker
            if 'ffd9' in hex_content:
                eof_pos = hex_content.rfind('ffd9') + 4
                if eof_pos < len(hex_content) - 2:
                    result['suspicious'] = True
                    result['details'].append("Hidden data found after JPEG EOF marker")
                
        elif hex_header.startswith('89504e47'):
            result['file_type'] = 'PNG'
            if result['extension'] != '.png':
                result['suspicious'] = True
                result['details'].append(f"File signature is PNG but has {result['extension']} extension")
                
            # Check for data after PNG IEND chunk
            if '49454e44ae426082' in hex_content:
                eof_pos = hex_content.rfind('49454e44ae426082') + 16
                if eof_pos < len(hex_content) - 2:
                    result['suspicious'] = True
                    result['details'].append("Hidden data found after PNG IEND chunk")
                
        elif hex_header.startswith('47494638'):
            result['file_type'] = 'GIF'
            if result['extension'] != '.gif':
                result['suspicious'] = True
                result['details'].append(f"File signature is GIF but has {result['extension']} extension")
                
        elif hex_header.startswith('424d'):
            result['file_type'] = 'BMP'
            if result['extension'] != '.bmp':
                result['suspicious'] = True
                result['details'].append(f"File signature is BMP but has {result['extension']} extension")
        
        # PDF files
        elif hex_header.startswith('25504446'):
            result['file_type'] = 'PDF'
            if result['extension'] != '.pdf':
                result['suspicious'] = True
                result['details'].append(f"File signature is PDF but has {result['extension']} extension")
        
        # ZIP/Office Document
        elif hex_header.startswith('504b0304'):
            if '776f72642f' in hex_content:  # 'word/' in content
                result['file_type'] = 'DOCX'
                if result['extension'] != '.docx':
                    result['suspicious'] = True
                    result['details'].append(f"File signature is DOCX but has {result['extension']} extension")
            elif '786c2f' in hex_content:  # 'xl/' in content
                result['file_type'] = 'XLSX'
                if result['extension'] != '.xlsx':
                    result['suspicious'] = True
                    result['details'].append(f"File signature is XLSX but has {result['extension']} extension")
            elif '7070742f' in hex_content:  # 'ppt/' in content
                result['file_type'] = 'PPTX'
                if result['extension'] != '.pptx':
                    result['suspicious'] = True
                    result['details'].append(f"File signature is PPTX but has {result['extension']} extension")
            else:
                result['file_type'] = 'ZIP'
                if result['extension'] != '.zip':
                    result['suspicious'] = True
                    result['details'].append(f"File signature is ZIP but has {result['extension']} extension")
        
        # MP3 files
        elif hex_header.startswith('494433') or hex_header.startswith('fffb'):
            result['file_type'] = 'MP3'
            if result['extension'] != '.mp3':
                result['suspicious'] = True
                result['details'].append(f"File signature is MP3 but has {result['extension']} extension")
        
        # MP4 files
        elif '66747970' in binascii.hexlify(header[4:12]).decode('ascii'):  # 'ftyp' in header
            result['file_type'] = 'MP4'
            if result['extension'] != '.mp4':
                result['suspicious'] = True
                result['details'].append(f"File signature is MP4 but has {result['extension']} extension")
        
        # MS Office legacy document
        elif hex_header.startswith('d0cf11e0'):
            result['file_type'] = 'MS Office document'
            if result['extension'] not in ['.doc', '.xls', '.ppt']:
                result['suspicious'] = True
                result['details'].append(f"File signature is MS Office document but has {result['extension']} extension")
        
        # RAR archives
        elif hex_header.startswith('526172211a07'):
            result['file_type'] = 'RAR'
            if result['extension'] != '.rar':
                result['suspicious'] = True
                result['details'].append(f"File signature is RAR but has {result['extension']} extension")
        
        # 7z archives
        elif hex_header.startswith('377abcaf271c'):
            result['file_type'] = '7Z'
            if result['extension'] != '.7z':
                result['suspicious'] = True
                result['details'].append(f"File signature is 7Z but has {result['extension']} extension")
        
        # GZIP files
        elif hex_header.startswith('1f8b08'):
            result['file_type'] = 'GZIP'
            if result['extension'] != '.gz':
                result['suspicious'] = True
                result['details'].append(f"File signature is GZIP but has {result['extension']} extension")
        
        # BZIP2 files
        elif hex_header.startswith('425a68'):
            result['file_type'] = 'BZIP2'
            if result['extension'] != '.bz2':
                result['suspicious'] = True
                result['details'].append(f"File signature is BZIP2 but has {result['extension']} extension")
        
        # XZ files
        elif hex_header.startswith('fd377a585a00'):
            result['file_type'] = 'XZ'
            if result['extension'] != '.xz':
                result['suspicious'] = True
                result['details'].append(f"File signature is XZ but has {result['extension']} extension")
                
        # RTF files
        elif hex_header.startswith('7b5c727466'):  # {\\rtf
            result['file_type'] = 'RTF'
            if result['extension'] != '.rtf':
                result['suspicious'] = True
                result['details'].append(f"File signature is RTF but has {result['extension']} extension")
        
        # Check for plaintext files
        elif all(32 <= int(hex_content[i:i+2], 16) <= 126 or int(hex_content[i:i+2], 16) in (9, 10, 13) 
                for i in range(0, min(32, len(hex_content)), 2)):
            
            # XML files
            if hex_header.startswith('3c3f786d6c') or b'<?xml' in header:  # <?xml
                result['file_type'] = 'XML'
                if result['extension'] != '.xml':
                    result['suspicious'] = True
                    result['details'].append(f"File signature is XML but has {result['extension']} extension")
            
            # HTML files
            elif b'<html' in header.lower() or b'<!doctype html' in header.lower():
                result['file_type'] = 'HTML'
                if result['extension'] not in ['.html', '.htm']:
                    result['suspicious'] = True
                    result['details'].append(f"File signature is HTML but has {result['extension']} extension")
            
            # JSON files
            elif header.startswith(b'{"') or header.startswith(b'['):
                result['file_type'] = 'JSON'
                if result['extension'] != '.json':
                    result['suspicious'] = True
                    result['details'].append(f"File signature is JSON but has {result['extension']} extension")
            
            # Plain text
            else:
                result['file_type'] = 'Text'
                if result['extension'] not in ['.txt', '.csv', '.log', '.md']:
                    result['suspicious'] = True
                    result['details'].append(f"File appears to be plain text but has {result['extension']} extension")
                    
    except Exception as e:
        result['suspicious'] = True
        result['details'].append(f"Error analyzing file: {str(e)}")
    
    return result