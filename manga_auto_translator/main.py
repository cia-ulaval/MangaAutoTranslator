from manga_auto_translator.cli_args import parse_args
from manga_auto_translator.file_ops import ScanIOManager
from manga_auto_translator.pipeline import TranslationPipeline


def cli():
    input_path, output_path = parse_args()
    scans = ScanIOManager.load_scans(input_path)

    pipeline = TranslationPipeline(scans)
    pipeline.run()

    # ScanIOManager.export_scans(output_path, scans)


if __name__ == '__main__':
    cli()
