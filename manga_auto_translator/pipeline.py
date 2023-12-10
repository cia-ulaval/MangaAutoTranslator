from typing import Sequence
from manga_auto_translator.segmentation.segmentation import SegmentationStrategy
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.ocr import OcrStrategy
from manga_auto_translator.postProcessSegmentation.postProcessSegmentation import PostProcessSegmentationStrategy
from manga_auto_translator.translation import TranslationStrategy


class TranslationPipeline:
    def __init__(self, scans: Sequence[Scan], segmentation_strategy:SegmentationStrategy,post_process_segmentation_strategy:PostProcessSegmentationStrategy,
                 ocr_strategy: OcrStrategy, translation_strategy: TranslationStrategy) -> None:
        self.scans = scans
        self.segmentation_strategy = segmentation_strategy
        self.post_process_segmentation_strategy = post_process_segmentation_strategy
        self.ocr_strategy = ocr_strategy
        self.translation_strategy = translation_strategy

    def run(self):
        self.segmentation()
        self.postprocess_segmentation()
        self.ocr()
        self.translation()
        self.postprocess_scan()

    def segmentation(self):
        self.segmentation_strategy.run(self.scans)

    def postprocess_segmentation(self):
        self.post_process_segmentation_strategy.run(self.scans)

    def ocr(self):
        self.ocr_strategy.run(self.scans)

    def translation(self):
        self.translation_strategy.run(self.scans)

    def postprocess_scan(self):
        pass
