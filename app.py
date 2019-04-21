from pathlib import Path
from shutil import rmtree
from uuid import uuid4
import re
import click


class App:
    def __init__(self, out_dir, num_files):
        self.out_path = Path(out_dir)
        self.num_files = num_files


    def generate(self):
        self._prepare_dir()
        next_name = 'file_00000000.py'
        self._generate_file('begin.py', next_name)
        for file_idx in range(self.num_files - 1):
            cur_name = next_name
            next_name = f'file_{str(file_idx + 1).zfill(8)}.py'
            self._generate_file(cur_name, next_name)
        self._generate_file(next_name, 'end.py')
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
@click.option('--num-files', default=120,
    help="Number of intermediate files to generate")
def generate(out_dir, num_files):
    app = App(out_dir=out_dir, num_files=num_files)
    app.generate()


cli()
