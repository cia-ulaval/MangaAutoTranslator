from typing import Sequence
from abc import ABC, abstractmethod
from enum import Enum
from PIL import Image
import cv2
import numpy as np

from manga_auto_translator.data_structure import Scan


class PostprocessScanStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan]) -> None:
        raise NotImplemented()


class CraftV1(PostprocessScanStrategy):
    def __init__(self) -> None:
        self.craft_mdoel = None
    
    def run(self, scans: Sequence[Scan]) -> None:
        for bubble in [bubble for scan in scans for bubble in scan.bubbles]:
            mask = self._find_text_mask(bubble.original_img)
            cleared = self._clear_previous_text(bubble.original_img, mask)
            bubble.translated_img = self._add_new_text(cleared, mask, bubble.translated_text)

    def _find_text_mask(self, image: Image.Image) -> Sequence[Sequence[bool]]:
        preds = self.craft_model.detect_text(image)

        ...

        mask = np.zeros_like(np.array(image)[:, :, 0])

        for rect in preds_rect:
            cropped = image.crop(rect)
            mask = cv2.threshold(cropped, cv2.BINARY+cv2.OSU)
            if np.median(mask) > np.mean(mask):
                mask = ~mask

    def _clear_previous_text(self, image: Image.Image, mask: Sequence[Sequence[bool]]) -> Sequence[Sequence[int]]:
        

        cv2.inpaint()
    
    def _add_new_text(self, image: Sequence[Sequence[int]], mask: Sequence[Sequence[bool]], text: str):
        pass


class PostprocessScanStrategyFactory:
    @abstractmethod
    def create(self, strategy: str) -> PostprocessScanStrategy:
        return AvailablePostprocessScanStrategies[self.strategy].value()


class AvailablePostprocessScanStrategies(Enum):
    CRAFT_V1 = CraftV1


ALLOWED_POSTPROCESS_SCAN_OPTIONS = [strategy.name for strategy in list(AvailablePostprocessScanStrategies)]