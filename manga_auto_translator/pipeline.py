from typing import Sequence
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.ocr import OcrStrategy
from manga_auto_translator.translation import TranslationStrategy
from manga_auto_translator.postprocess_scan import PostprocessScanStrategy


class TranslationPipeline:
    def __init__(
            self, 
            scans: Sequence[Scan], 
            ocr_strategy: OcrStrategy, 
            translation_strategy: TranslationStrategy,
            postprocess_scan_strategy: PostprocessScanStrategy,
    ) -> None:
        self.scans = scans
        self.ocr_strategy = ocr_strategy
        self.translation_strategy = translation_strategy
        self.postprocess_scan_strategy = postprocess_scan_strategy

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
        self.ocr_strategy.run(self.scans)

    def translation(self):
        self.translation_strategy.run(self.scans)

    def postprocess_scan(self):
        self.postprocess_scan_strategy.run(self.scans)
