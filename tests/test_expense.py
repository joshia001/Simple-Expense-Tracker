# tests/test_expense.py
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from expense_tracker import DB_READ_ERROR, SUCCESS, __app_name__, __version__, cli, tracker

runner = CliRunner()

def test_version():
    # .invoke() will run the application with specified inputs in a controlled environment. The output will be stored as a Result Object in result.
    result = runner.invoke(cli.app, ["--version"])
    
    # Define what we count as a success
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path: Path):
    expense = [{"Description":"Pay for Habibti", "Amount": 300.0, "Category": "General/Unassigned", "ID": 1}] # Excluded date for later date/time module use,Added amount as double for later arithmetic, included category as string (MAY REQUIRE CHANGE OF TYPE TO ENUM)
    db_file = tmp_path / "expense.json"
    with db_file.open("w") as db:
        json.dump(expense, db, indent=4)
    return db_file

test_data1 = {
    "description" : ["MSY", "Technology"],
    "amount": 350.0,
    "expense": {
        "Description": "MSY Technology.",
        "Amount": 350.0,
        # "Category": "General/Unassigned",
        # "ID": 2,
    },
}

test_data2 = {
    "description" : ["Zaatar for za habibdi"],
    "amount": 69.69,
    "expense": {
        "Description": "Zaatar for za habibdi.",
        "Amount": 69.69,
        # "Category": "General/Unassigned",
        # "ID": 3,
    },
}    

@pytest.mark.parametrize(
    "description, amount, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1['amount'],
            (test_data1["expense"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2['amount'],
            (test_data2["expense"], SUCCESS),
        )
    ]
)
def test_add(mock_json_file, description, amount, expected):
    expenser = tracker.Expenser(mock_json_file)
    assert expenser.add(description, amount) == expected
    read = expenser._db_handler.read_expenses()
    assert len(read.expense_list) == 2
    