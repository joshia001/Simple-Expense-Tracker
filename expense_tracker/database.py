"""This module provides the Expense Tracker database functionality."""
# expense_tracker/database.py

import configparser
from pathlib import Path

from expense_tracker import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_expense.json"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the expense database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create the expense database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR