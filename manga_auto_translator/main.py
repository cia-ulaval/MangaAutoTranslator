from cli_args import parse_args
from file_ops import load_scans, export_scans
from pipeline import run_pipeline


def cli():
    args = parse_args()
    scans = load_scans(args.input)
    
    for scan in scans:
        run_pipeline(scan)
    
    # export_scans(args.output, scans)


if __name__ == '__main__':
    cli()
