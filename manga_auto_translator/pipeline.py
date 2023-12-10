from typing import Sequence
from manga_auto_translator.segmentation.segmentation import SegmentationStrategy
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.ocr import OcrStrategy
from manga_auto_translator.postProcessSegmentation.postProcessSegmentation import PostProcessSegmentation
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
        print('segmentation : ')
        self.segmentation_strategy.run(self.scans)
        print(self.scans[0].segm_mask)

    def postprocess_segmentation(self):
        print('post process segmentation : ')
        self.post_process_segmentation_strategy.run(self.scans)
        print(self.scans[0].bubbles)

    def ocr(self):
        print('ocr : ')
        self.ocr_strategy.run(self.scans)
        print([bubble.inferred_text for bubble in self.scans[0].bubbles])

    def translation(self):
        self.translation_strategy.run(self.scans)
        print([bubble.translated_text for bubble in self.scans[0].bubbles])

    def postprocess_scan(self):
        pass
