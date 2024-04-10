import os
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener

def parse_date(date_str):
    date_format = "%Y:%m:%d %H:%M:%S"
    return datetime.strptime(date_str, date_format)

def parse_image_exif_date(exif_info):
    if 'DateTimeOriginal' in exif_info:
        date_str = exif_info['DateTimeOriginal']
        return parse_date(date_str)
    elif 'DateTime' in exif_info:
        date_str = exif_info['DateTime']
        return parse_date(date_str)
    else:
        return None

def parse_image_capture_time(file_path):
    with Image.open(file_path) as img:
        exif_data = img.getexif()

        if exif_data:
            exif_info = {TAGS[k]: v for k, v in exif_data.items() if k in TAGS}
            capture_time = parse_image_exif_date(exif_info)
        else:
            capture_time = None

        return capture_time

def rename(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for input_filename in os.listdir(input_path):
        full_input_filename = os.path.join(input_path, input_filename)
        full_output_filename = None

        try:
            capture_time = parse_image_capture_time(full_input_filename)

            if capture_time:
                output_filename = capture_time.strftime("%Y%m%d_%H%M%S") + "_" + input_filename
            else:
                output_filename = "99999999_999999" + "_" + input_filename

            full_output_filename = os.path.join(output_path, output_filename)

        except Exception as e:
            print(f"Error processing {input_filename}: {e}")

        if full_output_filename:
            os.rename(full_input_filename, full_output_filename)
            print(f"Renamed {input_filename} to {full_output_filename}")

if __name__ == "__main__":
    register_heif_opener()

    input_path = input("Enter the input path: ")
    output_path = input("Enter the output path: ")

    rename(input_path, output_path)
