"""Expense Tracker entry point script"""
# expense_tracker/__main__.py

from expense_tracker import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)
    
if __name__ == "__main__":
    main()