import os
from PIL import Image
import numpy as np
from data_structure import Scan


allowed_extensions = ['.png', '.jpg', '.jpeg']


def load_scans(directory: str) -> list:
    scans = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name) 

        if not validate_img_path(file_path):
            continue

        with open(file_path) as img_file:
            pil_image = Image.open(img_file)
            # making sure the image is black and white
            pil_image = pil_image.convert('L')
            img_array = np.array(pil_image)
            scan = Scan(img_array)
            scans.append(scan)
    
    return scans


def export_scans(directory: str, scans: list) -> None:
    raise NotImplemented("Implement this for exporting the scans.")


def validate_img_path(path: str) -> bool:
    if not os.path.isfile(path):
        return False

    valid_file_extension = any(path.endswith(ext) for ext in allowed_extensions)
    if not valid_file_extension:
        return False
    
    return True
