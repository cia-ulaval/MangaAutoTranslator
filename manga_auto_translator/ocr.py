from abc import ABC, abstractmethod
from PIL import Image
from manga_auto_translator.data_structure import BubbleData


class OcrStrategy(ABC):
    @abstractmethod
    def run(self, bubble: BubbleData) -> None:
        raise NotImplemented()


class MangaOcr(OcrStrategy):
    def __init__(self) -> None:
        print('Loading MangaOcr...')
        from manga_ocr import MangaOcr
        self.model = MangaOcr()
    
    def run(self, bubble: BubbleData) -> None:
        pil_image = Image.fromarray(bubble.original_img)
        bubble.inferred_text = self.model(pil_image)


class OcrStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy

    def create(self) -> OcrStrategy:
        return available_strategies[self.selected]()


available_strategies = {
    'manga-ocr': MangaOcr,
}


ALLOWED_OCR_OPTIONS = list(available_strategies.keys())
