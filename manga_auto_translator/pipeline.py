from typing import Sequence
from manga_auto_translator.segmentation.segmentation import SegmentationStrategy
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.ocr import OcrStrategy
from manga_auto_translator.postProcessSegmentation.postProcessSegmentation import PostProcessSegmentationStrategy
from manga_auto_translator.translation import TranslationStrategy
from manga_auto_translator.post_process_scan import PostProcessScanStrategy


class TranslationPipeline:
    def __init__(self, scans: Sequence[Scan], segmentation_strategy:SegmentationStrategy,post_process_segmentation_strategy:PostProcessSegmentationStrategy,
                 ocr_strategy: OcrStrategy, translation_strategy: TranslationStrategy,post_process_scan_strategy:PostProcessScanStrategy) -> None:
        self.scans = scans
        self.segmentation_strategy = segmentation_strategy
        self.post_process_segmentation_strategy = post_process_segmentation_strategy
        self.ocr_strategy = ocr_strategy
        self.translation_strategy = translation_strategy
        self.postprocess_scan_strategy = post_process_scan_strategy

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
        self.postprocess_scan_strategy.run(self.scans)
