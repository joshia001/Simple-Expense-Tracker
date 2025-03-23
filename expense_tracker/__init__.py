"""Top-level package for Expense Tracker."""
# expense_tracker/__init__.py
# created by joshia001

# App metadata
__app_name__ = "expense_tracker"
__version__ = "0.1.0"

# Status/error codes
(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

# Error messages mapped to codes
ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    JSON_ERROR: "data format error",
    ID_ERROR: "expense id error", 
}