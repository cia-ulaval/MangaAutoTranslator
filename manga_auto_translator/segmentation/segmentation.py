from abc import ABC, abstractmethod
from typing import Sequence
from manga_auto_translator.data_structure import Scan
from enum import Enum
import torch
import manga_auto_translator.segmentation.config as config

class SegmentationStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan]) -> None:
        raise NotImplemented()
    
class SegmentationUnet(SegmentationStrategy):
    def __init__(self) -> None:
        print('Loading Unet...')
        from manga_auto_translator.segmentation.UNet import UNet 
        self.model = UNet()
        self.model.load_state_dict(torch.load(config.MODEL_PATH))
        self.model.to(config.DEVICE)
    
    def run(self, scans: Sequence[Scan]) -> None:
        for scanIndex in range(len(scans)):
            scan = scans[scanIndex]
            scans[scanIndex].segm_mask = self.model.predict(scan.original_img)
    
class SegmentationStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy

    def create(self) -> SegmentationStrategy:
        return AvailableSegmentationStrategies[self.selected].value()



class AvailableSegmentationStrategies(Enum):
    Unet = SegmentationUnet
    
ALLOWED_SEGMENTATION_OPTIONS = [strategy.name for strategy in list(AvailableSegmentationStrategies)]