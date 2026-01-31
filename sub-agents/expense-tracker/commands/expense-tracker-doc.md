Generate or check documentation for the Expense Tracker application.

## Arguments
- `$1`: Optional flag. Use `--check` to verify existing documentation, or omit to generate new documentation.

## Instructions

1. Read the `expense_tracker.py` file to understand the current implementation.

2. If `$1` is `--check`:
   - Look for an existing `README.md` file in the project root
   - Verify it accurately documents:
     - How to run the application
     - All menu options and features
     - The ExpenseTracker class API (methods and their parameters)
     - The data storage format (expenses.json schema)
   - Report any missing or outdated sections
   - Suggest updates if the code has changed

3. If `$1` is empty or not `--check`:
   - Generate a comprehensive README.md with:
     - Project title and description
     - Requirements (Python 3.x)
     - Usage instructions (`python expense_tracker.py`)
     - Feature list with descriptions
     - API reference for the ExpenseTracker class
     - Data format documentation
   - Ask the user before writing the file

## Output Format
Provide a clear summary of findings (for --check) or the proposed documentation (for generate).
