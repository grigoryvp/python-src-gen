from pathlib import Path
from shutil import rmtree
from uuid import uuid4
import re
import click


class App:


    def __init__(
        self,
        out_dir,
        num_files,
        num_passes):

        self.out_path = Path(out_dir)
        self.num_files = num_files
        self.num_passes = num_passes


    def generate(self):
        self._prepare_dir()

        next_name = 'file_00000000.py'
        self._generate_file('begin.py', next_name)
        for file_idx in range(self.num_files - 1):
            cur_name = next_name
            next_name = f'file_{str(file_idx + 1).zfill(8)}.py'
            self._generate_file(cur_name, next_name)
        self._generate_file(next_name, 'end.py')
        self._generate_file('end.py', 'bug.py')
        (self.out_path / 'bug.py').write_text(
            "def test(arg: str): print(arg)")


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
            module_name = re.sub(r'\.py$', '', import_name)
            text += f'import {module_name}'
        text += '\n\ndef test(arg: int):'
        if import_name:
            next_name = 'pass_00000000'
            text += f'\n    {next_name} = arg'
            for pass_idx in range(self.num_passes - 1):
                cur_name = next_name
                next_name = f'pass_{str(pass_idx + 1).zfill(8)}'
                text += f'\n    {next_name} = {cur_name}'
            text += f'\n    {module_name}.test({next_name})'
        else:
            text += '\n    pass'
        text += '\n'
        path.write_text(text)


@click.group()
def cli(): pass


@cli.command()
@click.option('--out-dir', default='./out',
    type=click.Path(resolve_path=True),
    help="Directory path where to generate output")
@click.option('--num-files', default=100,
    type=click.IntRange(min=0, max=100000),
    help="Number of intermediate files to generate")
@click.option('--num-passes', default=100,
    type=click.IntRange(min=1, max=100000),
    help="Number of internal passes per file")
def generate(out_dir, num_files, num_passes):
    app = App(
        out_dir=out_dir,
        num_files=num_files,
        num_passes=num_passes)
    app.generate()


cli()
