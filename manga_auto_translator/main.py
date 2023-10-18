from cli_args import parse_args
from file_ops import ScanIOManager
from pipeline import TranslationPipeline


def cli():
    input_path, output_path = parse_args()
    scans = ScanIOManager.load_scans(input_path)

    pipeline = TranslationPipeline(scans)
    pipeline.run()

    # ScanIOManager.export_scans(output_path, scans)


if __name__ == '__main__':
    cli()
