import click
from manga_auto_translator.file_ops import ScanIOManager
from manga_auto_translator.pipeline import TranslationPipeline


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
def cli(input_path, output_path):
    scans = ScanIOManager.load_scans(input_path)

    pipeline = TranslationPipeline(scans)
    pipeline.run()

    # ScanIOManager.export_scans(output_path, scans)


if __name__ == '__main__':
    cli()
