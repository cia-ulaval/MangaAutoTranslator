from abc import ABC, abstractmethod

from manga_ocr import MangaOcr
from PIL import Image

from manga_auto_translator.data_structure import BubbleData


class OcrStrategy(ABC):
    @abstractmethod
    def run(self, bubble: BubbleData) -> None:
        raise NotImplemented()


class MangaOcr(OcrStrategy):
    def __init__(self) -> None:
        self.model = MangaOcr()
    
    def run(self, bubble: BubbleData) -> None:
        pil_image = Image.fromarray(bubble.original_img)
        bubble.inferred_text = self.model(pil_image)


class OcrStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy
        self.strategies = {
            'manga-ocr': MangaOcr,
        }

    def create(self) -> OcrStrategy:
        return self.strategies[self.selected]()
