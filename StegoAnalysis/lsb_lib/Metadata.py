from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
from datetime import datetime
from geopy.geocoders import Nominatim

def Metadata_extract_image(image_path):
    def extract_image(image_path):
        try:
            file_extension = os.path.basename(image_path).split('.')[-1]
            if file_extension.upper() not in ['JPG', 'JPEG', 'PNG']:
                return f"Unsupported file format: {file_extension}"
            
            img = Image.open(image_path)
            exif_data = img._getexif()
            metadata = {}
            if exif_data:
                for tagid, value in exif_data.items():
                    tagname = TAGS.get(tagid, tagid)
                    if isinstance(value, bytes):
                        try:
                            value = value.decode()
                        except:
                            value = f"Binary data of length {len(value)}"
                    metadata[tagname] = value
                gps_info = {}
                for key in exif_data:
                    tag = TAGS.get(key)
                    if tag == 'GPSInfo':
                        for t in exif_data[key]:
                            sub_tag = GPSTAGS.get(t, t)
                            gps_info[sub_tag] = exif_data[key][t]
                not_format_gps = {}
                for key, value in gps_info.items():
                    if isinstance(value, bytes):
                        try:
                            value = value.decode()
                        except:
                            value = f"Binary data of length {len(value)}"
                    gps_info[key] = value
                not_format_gps = gps_info.copy()
                    
                if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
                    gps_info['GPSLatitude'] = format_gps_value(gps_info['GPSLatitude'])
                    gps_info['GPSLongitude'] = format_gps_value(gps_info['GPSLongitude'])
                metadata['GPSInfo'] = gps_info
        
            metadata['Filename'] = os.path.basename(image_path)
            metadata['File Type'] = file_extension.upper()
            metadata['Creation DateTime'] = datetime.fromtimestamp(os.path.getctime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
            metadata['Location'] = get_location_from_image_simple(not_format_gps)
            return metadata
                
        except Exception as e:
            print(f"Error extracting metadata: {str(e)}")
            return None

    def format_gps_value(value):
        degrees, minutes, seconds = value
        return f"{degrees} deg {minutes}' {seconds}\""
        
    def decimal_coords(degrees, minutes, seconds, direction):
        decimal_degree = degrees + minutes / 60 + seconds / 3600
        if direction in ('S', 'W'):
            decimal_degree *= -1
        return decimal_degree

    def get_location_from_image_simple(gps_metadata):
        if not gps_metadata:
            return "Không có thông tin GPS"
        lat_info = gps_metadata.get('GPSLatitude')
        lon_info = gps_metadata.get('GPSLongitude')
        lat_dir = gps_metadata.get('GPSLatitudeRef', 'N')
        lon_dir = gps_metadata.get('GPSLongitudeRef', 'E')

        if lat_info and lon_info:
            try:
                lat = decimal_coords(*lat_info, lat_dir)
                lon = decimal_coords(*lon_info, lon_dir)

                geolocator = Nominatim(user_agent="image_location_finder")
                location = geolocator.reverse((lat, lon), language='vi', exactly_one=True)
                return location.address if location else "Không tìm thấy địa chỉ"
            except Exception as e:
                return f"Lỗi xử lý địa điểm: {str(e)}"
        return "Thiếu thông tin tọa độ"
    
    extract_image(image_path)