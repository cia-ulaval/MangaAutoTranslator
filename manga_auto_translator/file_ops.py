import os
from typing import Sequence, Union
from PIL import Image
import numpy as np
from manga_auto_translator.data_structure import Scan


class ScanIOManager:
    def __init__(self, allowed_extensions: Sequence[str] = ['.png', '.jpg', '.jpeg']) -> None:
        self.allowed_extensions = allowed_extensions

    def load_scans(self, directory: str, img_mode: Union[None, str]='L') -> list:
        scans = []

        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name) 

            if not self._validate_img_path(file_path):
                continue

            pil_image = Image.open(file_path)
            if img_mode is not None:
                pil_image = pil_image.convert(img_mode)
            img_array = np.array(pil_image)
            scan = Scan(img_array)
            scans.append(scan)
        
        return scans


    def export_scans(self, directory: str, scans: Sequence[Scan]) -> None:
        raise NotImplemented("Implement this for exporting the scans.")


    def _validate_img_path(self, path: str) -> bool:
        if not os.path.isfile(path):
            return False

        valid_file_extension = any(path.endswith(ext) for ext in self.allowed_extensions)
        if not valid_file_extension:
            return False
        
        return True


# static class
ScanIOManager = ScanIOManager()
