import os
from typing import Union
from PIL import Image
import numpy as np
from data_structure import Scan


allowed_extensions = ['.png', '.jpg', '.jpeg']


def load_scans(directory: str, img_mode: Union[None, str]='L') -> list:
    scans = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name) 

        if not validate_img_path(file_path):
            continue

        pil_image = Image.open(file_path)
        if img_mode is not None:
            pil_image = pil_image.convert(img_mode)
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
