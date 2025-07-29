import os
import sys
import logging
from PIL import Image 

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def is_png_file(filename):
    return filename.lower().endswith('.png')

def get_new_filename(filename):
    base, _ = os.path.splitext(filename)
    return base + '.jpeg'

def convert_png_to_jpeg(old_path, new_path):
 
    try:
        with Image.open(old_path) as img:
            rgb_img = img.convert('RGB')  
            rgb_img.save(new_path, 'JPEG')
            logging.info(f"Converted: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
            os.remove(old_path)  
    except Exception as e:
        logging.error(f"Failed to convert {old_path}: {e}")

def convert_png_extensions_in_folder(folder_path='.'):
    logging.info(f"Scanning folder: {os.path.abspath(folder_path)}")

    if not os.path.exists(folder_path):
        logging.error(f"Folder does not exist: {folder_path}")
        return

    if not os.path.isdir(folder_path):
        logging.error(f"Provided path is not a directory: {folder_path}")
        return

    files_changed = 0

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        if is_png_file(filename):
            new_filename = get_new_filename(filename)
            new_file_path = os.path.join(folder_path, new_filename)

            convert_png_to_jpeg(file_path, new_file_path)
            files_changed += 1

    logging.info(f"Total files converted: {files_changed}")

def main():
    setup_logging()

    folder = '.'
    if len(sys.argv) > 1:
        folder = sys.argv[1]

    convert_png_extensions_in_folder(folder)

if __name__ == "__main__":
    main()
