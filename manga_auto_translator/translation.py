from typing import Sequence
from abc import ABC, abstractmethod
from enum import Enum
from manga_auto_translator.data_structure import Scan


class TranslationStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan], lang_from: str, lang_to: str) -> None:
        raise NotImplemented()


class GoogleTraductionTranslation(TranslationStrategy):
    def __init__(self) -> None:
        print('Loading GoogleTraductionTranslation...')
        
    def run(self, scans: Sequence[Scan], lang_from: str, lang_to: str) -> None:
        from deep_translator import GoogleTranslator
        self.tranlator = GoogleTranslator(source=lang_from, target=lang_to)
        for bubble in [bubble for scan in scans for bubble in scan.bubbles]:
            bubble.translated_text = self.tranlator.translate(bubble.infered_text)


class TraductionStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy

    def create(self) -> TranslationStrategy:
        return AvailableTranslationStrategies[self.selected].value()


class AvailableTranslationStrategies(Enum):
    GOOGLE_TRADUCTION = GoogleTraductionTranslation


ALLOWED_TRANSLATION_OPTIONS = [strategy.name for strategy in list(AvailableTranslationStrategies)]
ALLOWED_TRANSLATION_SOURCE_LANG = ['ja', 'cn', 'ko']
ALLOWED_TRANSLATION_TARGET_LANG = ['fr', 'en']