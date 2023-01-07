"""Module entry point"""
from pathlib import Path
from typing import Optional

import click
from rich import print

from uwp_wgs import __version__
from .container import dump_container, load_container, Translator


@click.group
@click.version_option(__version__)
def main():
    pass


@main.command("list")
@click.argument(
    "input_dir",
    type=click.Path(
        file_okay=False, dir_okay=True, exists=True, resolve_path=True, path_type=Path
    ),
)
def list_files(input_dir: Path):
    container = load_container(input_dir)
    print(container)


@main.command("dump")
@click.option("--uppercase", is_flag=True, help="generate all uppercase filenames")
@click.option("--lowercase", is_flag=True, help="generate all lowercase filenames")
@click.argument(
    "input_dir",
    type=click.Path(
        file_okay=False, dir_okay=True, exists=True, resolve_path=True, path_type=Path
    ),
)
@click.argument(
    "output_dir",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True, path_type=Path),
)
def dump_files(input_dir: Path, output_dir: Path, lowercase: bool, uppercase: bool):
    container = load_container(input_dir)

    translator: Optional[Translator] = None
    if uppercase:
        translator = lambda p: p.with_name(p.name.upper())
    elif lowercase:
        translator = lambda p: p.with_name(p.name.lower())
    dump_container(container, output_dir, translator=translator)


if __name__ == "__main__":
    main()
