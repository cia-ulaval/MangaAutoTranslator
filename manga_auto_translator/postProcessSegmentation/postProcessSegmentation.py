from manga_auto_translator.data_structure import Scan,BubbleData
from typing import Sequence
from enum import Enum
from abc import ABC, abstractmethod
from manga_auto_translator.utils import prepare_plot
from copy import deepcopy
import scipy as  sp
import cv2




class PostProcessSegmentationStrategy(ABC):
    @abstractmethod
    def run(self, scans: Sequence[Scan]) -> None:
        raise NotImplemented()


class PawsPostProcessSegmentation:
	def __init__(self) -> None:
		pass


	def find_paws(self,data, smooth_radius=5, threshold=0.0001):
			data = sp.ndimage.uniform_filter(data, smooth_radius)
			thresh = data > threshold
			filled = sp.ndimage.morphology.binary_fill_holes(thresh)
			coded_paws, num_paws = sp.ndimage.label(filled)
			data_slices = sp.ndimage.find_objects(coded_paws)
			return data_slices


	def run(self,scans: Sequence[Scan]):
		for scanIndex in range(len(scans)):
			scan = scans[scanIndex]
			pawedImage = deepcopy(scan.segm_mask)
			paws = self.find_paws(scan.segm_mask)
			i=0
			bubbles = []
			for paw in paws:
				threshold = 50
				if paw[0].stop - paw[0].start > threshold and paw[1].stop - paw[1].start > threshold:
					paw = list(paw)
					pawedImage[paw[0],paw[1]] = 255
					# cv2.imwrite('testCase'+str(i)+'.png', scan.original_img[paw[0],paw[1]])
					bubble = BubbleData(scan.original_img[paw[0],paw[1]],paw)
					bubbles.append(bubble)
					i+=1
			scan.bubbles = bubbles
			# prepare_plot(scan.original_img,scan.segm_mask,pawedImage , str(i)+'postProcessSegmentation.png')


class PostProcessSegmentationStrategyFactory:
    def __init__(self, strategy: str) -> None:
        self.selected = strategy

    def create(self) -> PostProcessSegmentationStrategy:
        return AvailablePostProcessSegmentationStrategies[self.selected].value()


class AvailablePostProcessSegmentationStrategies(Enum):
    Paws = PawsPostProcessSegmentation


ALLOWED_POST_PROCESS_SEGMENTATION_OPTIONS = [strategy.name for strategy in list(AvailablePostProcessSegmentationStrategies)]
	
