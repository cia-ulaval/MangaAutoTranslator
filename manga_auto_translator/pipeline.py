from data_structure import Scan


def run_pipeline(scan: Scan):
    segmentation(scan)
    postprocess_segmentation(scan)
    ocr(scan)
    translation(scan)
    postprocess_scan(scan)


def segmentation(scan: Scan):
    pass


def postprocess_segmentation(scan: Scan):
    pass


def ocr(scan: Scan):
    pass


def translation(scan: Scan):
    pass


def postprocess_scan(scan: Scan):
    pass