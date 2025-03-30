"""This module provides the Expense Tracker database functionality."""
# expense_tracker/database.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from expense_tracker import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

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
    
class DBResponse(NamedTuple):
    expense_list: List[Dict[str, Any]]
    error: int
    
class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
    
    def read_expenses(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError: # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError: # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)
        
    def write_expenses(self, expense_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(expense_list, db, indent=4)
            return DBResponse(expense_list, SUCCESS)
        except OSError: # Catch file IO problems
            return DBResponse(expense_list, DB_WRITE_ERROR)