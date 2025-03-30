# tests/test_expense.py
import json

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
def mock_json_file(tmp_path):
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
        "Category": "General/Unassigned",
        "ID": 2,
    },
}

test_data2 = {
    "description" : [],
    "amount": ,
    "expense": {
        "Description": ".",
        "Amount": ,
        "Category": "General/Unassigned",
        "ID": 3,
    },
}    