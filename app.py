from pathlib import Path
import click


class App:
    def __init__(self, out_dir):
        self.out_path = Path(out_dir)


    def generate(self):
        self._prepare_dir()


    def _prepare_dir(self):
        try:
            self.out_path.mkdir()
        except FileExistsError:
            pass


@click.group()
def cli(): pass


@cli.command()
@click.option('--out-dir', default='./out',
    type=click.Path(resolve_path=True),
    help="Directory path where to generate output")
def generate(out_dir):
    app = App(out_dir=out_dir)
    app.generate()


cli()
