import click
from manga_auto_translator.file_ops import ScanIOManager
from manga_auto_translator.pipeline import TranslationPipeline
from manga_auto_translator.ocr import OcrStrategyFactory, ALLOWED_OCR_OPTIONS
from manga_auto_translator.translation import TraductionStrategyFactory, ALLOWED_TRANSLATION_OPTIONS, ALLOWED_TRANSLATION_SOURCE_LANG, ALLOWED_TRANSLATION_TARGET_LANG


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
def cli(input_path, output_path, ocr, translation_api, lang_from, lang_to):
    scans = ScanIOManager.load_scans(input_path)

    ocr_strategy = OcrStrategyFactory(strategy=ocr).create()
    translation_strategy = TraductionStrategyFactory.create(translation_api, lang_from, lang_to)

    pipeline = TranslationPipeline(scans, ocr_strategy, translation_strategy)
    pipeline.run()

    # ScanIOManager.export_scans(output_path, scans)


if __name__ == '__main__':
    cli()
