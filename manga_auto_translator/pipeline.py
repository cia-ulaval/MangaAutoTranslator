from typing import Sequence
from data_structure import Scan


class TranslationPipeline:
    def __init__(self, scans: Sequence[Scan]) -> None:
        self.scans = scans

    def run(self):
        self.segmentation()
        self.postprocess_segmentation()
        self.ocr()
        self.translation()
        self.postprocess_scan()

    def segmentation(self):
        pass

    def postprocess_segmentation(self):
        pass

    def ocr(self):
        pass

    def translation(self):
        pass

    def postprocess_scan(self):
        pass
