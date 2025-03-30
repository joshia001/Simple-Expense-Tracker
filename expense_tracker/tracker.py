"""This module provides the Expense Tracker model-controller."""
# expense_tracker/tracker.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from expense_tracker.database import DatabaseHandler

class CurrentExpense(NamedTuple):
    expense: Dict[str, Any]
    error: int
    
class Expenser:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)