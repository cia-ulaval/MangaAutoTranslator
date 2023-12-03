from typing import Sequence
from abc import ABC, abstractmethod
from enum import Enum
from deep_translator import GoogleTranslator
from manga_auto_translator.data_structure import Scan


class TranslationStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan], lang_from: str, lang_to: str) -> None:
        raise NotImplemented()


class GoogleTraductionTranslation(TranslationStrategy):
    def __init__(self, lang_from: str, lang_to: str) -> None:
        print('Loading GoogleTraductionTranslation...')
        self.tranlator = GoogleTranslator(source=lang_from, target=lang_to)
        
    def run(self, scans: Sequence[Scan]) -> None:
        for bubble in [bubble for scan in scans for bubble in scan.bubbles]:
            bubble.translated_text = self.tranlator.translate(bubble.infered_text)


class TraductionStrategyFactory:

    @staticmethod
    def create(strategy: str, lang_from: str, lang_to: str) -> TranslationStrategy:
        return AvailableTranslationStrategies[strategy].value(lang_from, lang_to)


class AvailableTranslationStrategies(Enum):
    GOOGLE_TRADUCTION = GoogleTraductionTranslation


ALLOWED_TRANSLATION_OPTIONS = [strategy.name for strategy in list(AvailableTranslationStrategies)]
ALLOWED_TRANSLATION_SOURCE_LANG = ['ja', 'cn', 'ko']
ALLOWED_TRANSLATION_TARGET_LANG = ['fr', 'en']