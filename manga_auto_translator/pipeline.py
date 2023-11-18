from typing import Sequence
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.segmentation_Unet.pyimagesearch.model8 import UNet

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
        unet = UNet()
        for scanIndex in range(len(self.scans)):
            scan = self.scans[scanIndex]
            self.scans[scanIndex].segm_mask = unet.predict(scan.original_img)

    def postprocess_segmentation(self):
        pass

    def ocr(self):
        pass

    def translation(self):
        pass

    def postprocess_scan(self):
        pass
