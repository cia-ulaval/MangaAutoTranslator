from argparse import ArgumentParser
from file_ops import load_scans, export_scans
from pipeline import run_pipeline


def cli():
    argument_parser = ArgumentParser(description="Automatic translator for manga/manhwa/manhua")
    argument_parser.add_argument('--input', type=str, default='./', help='Folder where the original scans are located')
    argument_parser.add_argument('--output', type=str, default='./scans-converted', help='Folder to output the converted scans')
    args = argument_parser.parse_args()

    scans = load_scans(args.input)
    for scan in scans:
        run_pipeline(scan)
    
    # export_scans(args.output, scans)


if __name__ == '__main__':
    cli()
