from pathlib import Path
import click


@click.group()
def cli(): pass


@cli.command()
@click.option('--out-dir', default='./out',
    type=click.Path(resolve_path=True),
    help="Directory path where to generate output")
def generate(out_dir):
    root = Path(out_dir)
    try:
        root.mkdir()
    except FileExistsError:
        pass


cli()
