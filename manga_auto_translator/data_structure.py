class BubbleData:
    _init_counter = 0

    def __init__(self, img, coordinates: list) -> None:
        self.id = BubbleData._init_counter
        BubbleData._init_counter += 1
        self.original_img = img
        self.coordinates = coordinates
        self.infered_text = None
        self.translated_text = None
        self.translated_img = None

        @property
        def width(self):
            return self.coordinates[3] - self.coordinates[1]

        @property
        def height(self):
            return self.coordinates[2] - self.coordinates[0]


class Scan:
    def __init__(self, original_img) -> None:
        self.original_img = original_img
        self.segm_mask = None
        self.bubbles = None
