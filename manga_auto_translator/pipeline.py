from typing import Sequence
import manga_auto_translator.segmentation.config as config
import torch
from manga_auto_translator.segmentation.UNet import UNet 
from manga_auto_translator.data_structure import Scan
from manga_auto_translator.ocr import OcrStrategy
from manga_auto_translator.postProcessSegmentation.postProcessSegmentation import PostProcessSegmentation


class TranslationPipeline:
    def __init__(self, scans: Sequence[Scan], ocr_strategy: OcrStrategy) -> None:
        self.scans = scans
        self.unet = UNet()
        self.unet.load_state_dict(torch.load(config.MODEL_PATH))
        self.unet.to(config.DEVICE)
        self.ocr_strategy = ocr_strategy
        self.postProcessSegmentation = PostProcessSegmentation()

    def run(self):
        self.segmentation()
        self.postprocess_segmentation()
        self.ocr()
        self.translation()
        self.postprocess_scan()

    def segmentation(self):
        for scanIndex in range(len(self.scans)):
            scan = self.scans[scanIndex]
            self.scans[scanIndex].segm_mask = self.unet.predict(scan.original_img)
        print(self.scans[0].segm_mask)

    def postprocess_segmentation(self):
        self.postProcessSegmentation.treatScans(self.scans)
        print(self.scans[0].bubbles)

    def ocr(self):
        self.ocr_strategy.run(self.scans)

    def translation(self):
        pass

    def postprocess_scan(self):
        pass
