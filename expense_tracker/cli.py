"""This module provides the Expense Tracker CLI."""
# expense_tracker/cli.py

from typing import Optional

import typer

from expense_tracker import __app_name__, __version__

app = typer.Typer(help="A simple CLI expense tracker.")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback = _version_callback,
        is_eager = True,
    )
) -> None:
    return