import typer
from typing_extensions import Annotated
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from .validate import validate

console = Console()
app = typer.Typer()


@app.callback()
def callback():
    """
    Welcome to datajoint-file-validator!
    """


def show_table():
    table = Table("Name", "Item")
    table.add_row("Rick", "Portal Gun")
    table.add_row("Morty", "Plumbus")
    console.print(table)


def open_file(path: str):
    """
    Open a file at PATH in the default app.
    """
    rprint(f":left_speech_bubble:  Opening file {path}")
    typer.launch(path, locate=True)


def read_file(path: Annotated[typer.FileText, typer.Option()]):
    """
    Reads lines from a file at PATH.
    """
    for line in path:
        rprint(f"Config line: {path}")


def main(name: str, lastname: str = "", formal: bool = False):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        rprint(f"Good day Ms. {name} {lastname}.")
    else:
        rprint(f"Hello {name} {lastname}")


@app.command()
def validate(
    target: Annotated[str, typer.Argument(..., exists=True)],
    manifest: Annotated[typer.FileText, typer.Argument(..., exists=True)],
    raise_err: bool = False,
):
    """
    Validate a target against a manifest.
    """
    success, report = validate(
        target, manifest, verbose=False, raise_err=raise_err
    )
    if success:
        rprint(":heavy_check_mark: Validation successful!")
    else:
        rprint(":x: Validation failed!")
        rprint(table_from_report(report))