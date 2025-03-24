import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from Metadata import Metadata_extract_image

def decimal_coords(degrees, minutes, seconds, direction):
    decimal_degree = degrees + minutes / 60 + seconds / 3600
    if direction in ('S', 'W'):
        decimal_degree *= -1
    return decimal_degree

def get_location_from_image_simple(image_path):
    gps_metadata = Metadata_extract_image(image_path)
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
            return location.address
        except Exception:
            return "Lỗi xử lý địa điểm"
    return "Thiếu thông tin tọa độ"   