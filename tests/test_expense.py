# tests/test_expense.py

from typer.testing import CliRunner

from expense_tracker import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    # .invoke() will run the application with specified inputs in a controlled environment. The output will be stored as a Result Object in result.
    result = runner.invoke(cli.app, ["--version"])
    
    # Define what we count as a success
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout