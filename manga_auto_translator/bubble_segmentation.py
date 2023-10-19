from typing import Sequence
from PIL import Image
import numpy as np


class SegmentationStrategy:
    def segment_batch(self, batch: Sequence[Sequence[Sequence[int]]]) -> Sequence[Sequence[Sequence[bool]]]:
        raise NotImplemented()


class DummySegmentation(SegmentationStrategy):
    def segment_batch(self, batch: Sequence[Sequence[Sequence[int]]]) -> Sequence[Sequence[Sequence[bool]]]:
        return np.where(batch >= 128, True, False)
    