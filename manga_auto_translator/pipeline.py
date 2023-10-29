from typing import Sequence
from manga_auto_translator.data_structure import Scan
from ocr import OcrStrategyFactory


class TranslationPipeline:
    def __init__(self, scans: Sequence[Scan], pipeline_args: dict) -> None:
        self.scans = scans
        self.ocr_strategy = OcrStrategyFactory(strategy=pipeline_args.get('ocr')).create()

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
