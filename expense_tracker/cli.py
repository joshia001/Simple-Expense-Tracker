"""This module provides the Expense Tracker CLI."""
# expense_tracker/cli.py

from pathlib import Path
from typing import List, Optional

import typer # type: ignore

from expense_tracker import ERRORS, __app_name__, __version__, config, database, tracker

app = typer.Typer(help="A simple CLI expense tracker.")

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="expense database location?",
    ),
) -> None:
    """Initialise the expense database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The expense database is {db_path}", fg = typer.colors.GREEN)

def get_expenser() -> tracker.Expenser:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "expense_tracker init"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return tracker.Expenser(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "expense_tracker init"',
            fg = typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    amount: float = typer.Option(0, "--amount", "-a", min = 0),
) -> None:
    """Add a new expense with a DESCRIPTION."""
    tracker = get_expenser()
    todo, error = tracker.add(description, amount)
    if error:
        typer.secho(
            f'Adding expense failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    
    typer.secho(
        f"""to-do: "{todo['Description']}" was added """
        f"""with amount: {amount}""",
        fg=typer.colors.GREEN,
    )

@app.command(name='list')
def list_all() -> None:
    """List all expenses"""
    tracker = get_expenser()
    expense_list = tracker.get_expense_list()
    if len(expense_list) == 0:
        typer.secho(
            "There are no tasks in the expense list yet", fg = typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nexpense list:\n", fg= typer.colors.BLUE, bold = True)
    columns = (
        "ID. ",
        "| Amount    ",
        "| Description"
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, expense in enumerate(expense_list, 1):
        desc, amount = expense.values()
        typer.secho(
            f"{id}{(len(columns[0])-len(str(id))) * ' '}"
            f"| {amount}{(len(columns[1]) - len(str(amount))-2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback = _version_callback,
        is_eager = True,
    )
) -> None:
    return