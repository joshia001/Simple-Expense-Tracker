"""This module provides the Expense Tracker model-controller."""
# expense_tracker/tracker.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

from expense_tracker import DB_READ_ERROR
from expense_tracker.database import DatabaseHandler, DBResponse

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

        read = self.get_current_expense()

        read.expense_list.append(expense)
        write = self._db_handler.write_expenses(read.expense_list)
        return CurrentExpense(expense, write.error)
    def get_expense_list(self) -> List[Dict[str, Any]]:
        """Return the current expense list."""

    def remove(self, item : str) -> CurrentExpense:
        """Removes Items from the database"""

        db_response = self.get_current_expense()

        expense_items = db_response.expense_list

        new_expense_items = []

        for index, (description, amount) in enumerate(expense_items):

            current_item_name = expense_items[index][description]
            if item == current_item_name[:-1]:
                continue
            new_expense_items.append(expense_items[index])


        if len(new_expense_items) == len(expense_items): 
            raise Exception("Item not in expense_items")
        
        db_response.expense_list = new_expense_items
        write = self._db_handler.write_expenses(db_response.expense_list)

        return write.error


    def get_items(self) -> List[dict[str,Any]]:
        db_response = self.get_current_expense()

        return db_response.expense_list

    def get_current_expense(self) -> DBResponse:
        """Gets the current expense from the database"""

        read = self._db_handler.read_expenses()
        if read.error == DB_READ_ERROR:
            return CurrentExpense(expense, read.error)
        return read


        read = self._db_handler.read_expenses()
        return read.expense_list