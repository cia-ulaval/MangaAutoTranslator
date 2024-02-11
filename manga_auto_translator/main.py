import click
from manga_auto_translator.file_ops import ScanIOManager
from manga_auto_translator.pipeline import TranslationPipeline
from manga_auto_translator.ocr import OcrStrategyFactory, ALLOWED_OCR_OPTIONS
from manga_auto_translator.segmentation.segmentation import SegmentationStrategyFactory,ALLOWED_SEGMENTATION_OPTIONS
from manga_auto_translator.translation import TraductionStrategyFactory, ALLOWED_TRANSLATION_OPTIONS, ALLOWED_TRANSLATION_SOURCE_LANG, ALLOWED_TRANSLATION_TARGET_LANG
from manga_auto_translator.postProcessSegmentation.postProcessSegmentation import ALLOWED_POST_PROCESS_SEGMENTATION_OPTIONS,PostProcessSegmentationStrategyFactory
from manga_auto_translator.post_process_scan import ALLOWED_POST_PROCESS_SCAN_OPTIONS,PostProcessScanStrategyFactory

@click.command(help="Automatic translator for manga/manhwa/manhua")
@click.option(
    '--input-path', '-i', 
    type=click.Path(exists=True, file_okay=False, dir_okay=True), 
    default='./', 
    help='Folder where the original scans are located.'
)
@click.option(
    '--output-path', '-o', 
    type=click.Path(dir_okay=True), 
    default='./scans-converted', 
    help='Folder to output the converted scans. If the folder does not exist, it will be created.'
)
@click.option(
    '--segmentation', 
    type=click.Choice(ALLOWED_SEGMENTATION_OPTIONS),
    default='Unet',
    help=f'Segmentation strategy to use for bubble detection'
)
@click.option(
    '--post-process-segmentation', 
    type=click.Choice(ALLOWED_POST_PROCESS_SEGMENTATION_OPTIONS),
    default='Paws',
    help=f'Post process segmentation strategy to transform blob of pixel into actual bubbles'
)
@click.option(
    '--ocr', 
    type=click.Choice(ALLOWED_OCR_OPTIONS),
    default='MANGA_OCR',
    help=f'OCR strategy to use for character recognition.'
)
@click.option(
    '--translation-api', '-t',
    type=click.Choice(ALLOWED_TRANSLATION_OPTIONS),
    default='GOOGLE_TRADUCTION',
    help='OCR strategy to use for character recognition.'
)
@click.option(
    '--lang-from',
    type=click.Choice(ALLOWED_TRANSLATION_SOURCE_LANG),
    default='ja',
    help='Original language to translate from'
)
@click.option(
    '--lang-to',
    type=click.Choice(ALLOWED_TRANSLATION_TARGET_LANG),
    default='fr',
    help='Language to translate to'
)
@click.option(
    '--post-process-scan', 
    type=click.Choice(ALLOWED_POST_PROCESS_SCAN_OPTIONS),
    default='Naive',
    help=f'Post process scan strategy to replace original text in bubble with translated text'
)

def cli(input_path, output_path, segmentation,post_process_segmentation,ocr, translation_api, lang_from, lang_to,post_process_scan):
    scans = ScanIOManager.load_scans(input_path)

    segmentation_strategy = SegmentationStrategyFactory(strategy=segmentation).create()
    post_process_segmentation_strategy = PostProcessSegmentationStrategyFactory(strategy=post_process_segmentation).create()
    ocr_strategy = OcrStrategyFactory(strategy=ocr).create()
    translation_strategy = TraductionStrategyFactory.create(translation_api, lang_from, lang_to)
    post_process_scan_strategy = PostProcessScanStrategyFactory(strategy=post_process_scan).create()
    
    pipeline = TranslationPipeline(scans,segmentation_strategy,post_process_segmentation_strategy, ocr_strategy, translation_strategy,post_process_scan_strategy)
    pipeline.run()

    ScanIOManager.export_scans(output_path, scans)


if __name__ == '__main__':
    cli()
