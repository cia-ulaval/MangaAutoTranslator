from typing import Sequence
from abc import ABC, abstractmethod
from enum import Enum
from PIL import Image
from manga_auto_translator.data_structure import Scan, BubbleData


class OcrStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan]) -> None:
        raise NotImplemented()


class MangaOcr(OcrStrategy):
    def __init__(self) -> None:
        print('Loading MangaOcr...')
        from manga_ocr import MangaOcr
        self.model = MangaOcr()
    
    def run(self, scans: Sequence[Scan]) -> None:
        for bubble in [bubble for scan in scans for bubble in scan.bubbles]:
            pil_image = Image.fromarray(bubble.original_img)
            bubble.inferred_text = self.model(pil_image)


class OcrStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy

    def create(self) -> OcrStrategy:
        return AvailableOcrStrategies[self.selected].value()


class AvailableOcrStrategies(Enum):
    MANGA_OCR = MangaOcr


ALLOWED_OCR_OPTIONS = [strategy.name for strategy in list(AvailableOcrStrategies)]
