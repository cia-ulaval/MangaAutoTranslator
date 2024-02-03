from manga_auto_translator.data_structure import Scan,BubbleData
from typing import Sequence
from enum import Enum
from abc import ABC, abstractmethod
from manga_auto_translator.utils import prepare_plot
from copy import deepcopy
import cv2
import scipy as  sp

class PostProcessScanStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan]) -> None:
        raise NotImplemented()


class NaivePostProcessScan:
    def __init__(self) -> None:
        pass


    def run(self,scans: Sequence[Scan]):
        i=0
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1 
        color = (0, 0, 0) 
        thickness = 1
        for scanIndex in range(len(scans)):
            scan = scans[scanIndex]
            translatedImage = deepcopy(scan.original_img)
            for bubble in scan.bubbles:
                translatedImage[bubble.coordinates[0],bubble.coordinates[1]] = 255
                translatedImage = cv2.putText(translatedImage,bubble.translated_text,(bubble.coordinates[1].start,bubble.coordinates[0].stop),
                                              font,fontScale,color,thickness,cv2.LINE_AA)
            scan.translated_img = translatedImage
            # cv2.imwrite('testCase'+str(i)+'.png',translatedImage)
            i+=1

class PostProcessScanStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy

    def create(self) -> PostProcessScanStrategy:
        return AvailablePostProcessScanStrategyStrategies[self.selected].value()

class AvailablePostProcessScanStrategyStrategies(Enum):
    Naive = NaivePostProcessScan


ALLOWED_POST_PROCESS_SCAN_OPTIONS = [strategy.name for strategy in list(AvailablePostProcessScanStrategyStrategies)]
	
