from argparse import ArgumentParser


def cli():
    argument_parser = ArgumentParser(description="Automatic translator for manga/manhwa/manhua")
    argument_parser.add_argument('--input', type=str, default='./', help='Folder where the original scans are located')
    argument_parser.add_argument('--output', type=str, default='./scans-converted', help='Folder to output the converted scans')
    args = argument_parser.parse_args()
    pass


if __name__ == '__main__':
    cli()
