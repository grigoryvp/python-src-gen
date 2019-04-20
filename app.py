from pathlib import Path
from shutil import rmtree
from uuid import uuid4
import re
import click


class App:
    def __init__(self, out_dir):
        self.out_path = Path(out_dir)


    def generate(self):
        self._prepare_dir()
        self._generate_file('begin.py', 'end.py')
        # Generate a number of file that import each other.
        self._generate_file('end.py')


    def _prepare_dir(self):
        try:
            rmtree(str(self.out_path), ignore_errors=True)
            self.out_path.mkdir()
        except FileExistsError:
            pass


    def _generate_file(self, name, import_name: str=None):
        path = self.out_path / name
        path.touch()
        text = ""
        if import_name:
            module_name = re.sub('\.py$', '', import_name)
            text += f'import {module_name}'
        text += '\n\ndef test(arg: int):'
        if import_name:
            text += f'\n    {module_name}.test(arg)'
        else:
            text += '\n    pass'
        path.write_text(text)


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
