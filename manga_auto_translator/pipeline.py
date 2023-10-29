from typing import Sequence
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.ocr import OcrStrategy


class TranslationPipeline:
    def __init__(self, scans: Sequence[Scan], ocr_strategy: OcrStrategy) -> None:
        self.scans = scans
        self.ocr_strategy = ocr_strategy

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
        [
            self.ocr_strategy.run(bubble) 
            for scan in self.scans 
            for bubble in scan.bubbles
        ]

    def translation(self):
        pass

    def postprocess_scan(self):
        pass
