from typing import Sequence, Union
from dataclasses import dataclass


@dataclass
class BubbleData:
    original_img: Sequence[Sequence[int]]
    coordinates: Sequence[int]
    infered_text: Union[None, str] = None
    translated_text: Union[None, str] = None
    translated_img: Union[None, Sequence[Sequence[int]]] = None

    def __post_init__(self):
        if not hasattr(BubbleData, '_init_counter'):
            BubbleData._init_counter: int = 0
        self.id: int = BubbleData._init_counter
        BubbleData._init_counter += 1

    @property
    def width(self):
        return self.coordinates[3] - self.coordinates[1]

    @property
    def height(self):
        return self.coordinates[2] - self.coordinates[0]


@dataclass
class Scan:
    def __init__(self, original_img: Sequence[Sequence[int]]) -> None:
        self.original_img: Sequence[Sequence[int]] = original_img
        self.segm_mask: Union[None, Sequence[Sequence[int]]] = None
        self.bubbles: Union[None, Sequence[BubbleData]] = None
