from typing import Sequence
import numpy as np
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.bubble_segmentation import SegmentationStrategy, DummySegmentation


class TranslationPipeline:
    def __init__(
            self, scans: Sequence[Scan], 
            segmentation_strategy: SegmentationStrategy=DummySegmentation()
    ) -> None:
        self.scans = scans
        self.segmentation_strategy = segmentation_strategy

    def run(self):
        self.segmentation()
        self.postprocess_segmentation()
        self.ocr()
        self.translation()
        self.postprocess_scan()

    def segmentation(self):
        img_batch = np.array([scan.original_img for scan in self.scans])
        mask_batch = self.segmentation_strategy.segment_batch(img_batch)
        for scan, mask in zip(self.scans, mask_batch):
            scan.segm_mask = mask

    def postprocess_segmentation(self):
        pass

    def ocr(self):
        pass

    def translation(self):
        pass

    def postprocess_scan(self):
        pass
