"""This module provides the Expense Tracker model-controller."""
# expense_tracker/tracker.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

from expense_tracker import DB_READ_ERROR
from expense_tracker.database import DatabaseHandler

class CurrentExpense(NamedTuple):
    expense: Dict[str, Any]
    error: int
    
class Expenser:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
        
    def add(self, description: List[str], amount: float) -> CurrentExpense:
        """Add a new expense to the database."""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        expense = {
            "Description": description_text,
            "Amount": amount,
        }
        read = self._db_handler.read_expenses()
        if read.error == DB_READ_ERROR:
            return CurrentExpense(expense, read.error)
        read.expense_list.append(expense)
        write = self._db_handler.write_expenses(read.expense_list)
        return CurrentExpense(expense, write.error)
        def get_todo_list(self) -> List[Dict[str, Any]]:
            """Return the current expense list."""