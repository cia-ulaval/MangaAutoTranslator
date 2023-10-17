class BubbleData:
    initCount = 0

    def __init__(self, img, coordinates) -> None:
        BubbleData.initCount += 1
        self.id = BubbleData.initCount
        self.original_img = img
        self.coordinates = coordinates
        self.infered_text = None
        self.translated_text = None
        self.translated_img = None


class Scan:
    def __init__(self, original_img) -> None:
        self.original_img = original_img
        self.segm_mask = None
        self.bubbles = None
