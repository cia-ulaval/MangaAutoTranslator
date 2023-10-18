import click


@click.command(help="Automatic translator for manga/manhwa/manhua")
@click.option(
    '--input', '-i', 
    type=click.Path(exists=True, file_okay=False, dir_okay=True), 
    default='./', 
    help='Folder where the original scans are located.'
)
@click.option(
    '--output', '-o', 
    type=click.Path(dir_okay=True), 
    default='./scans-converted', 
    help='Folder to output the converted scans. If the folder does not exist, it will be created.'
)
def parse_args(input, output):
    return input, output
