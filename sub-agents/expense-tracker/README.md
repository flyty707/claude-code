# Expense Tracker

A simple command-line expense tracking application written in Python. Track your daily expenses with categories, view spending summaries, and persist data to JSON files.

## Features

- Add expenses with amount, category, and description
- View all expenses in a formatted table
- Calculate total spending
- Persistent storage using JSON
- Auto-generated expense IDs and timestamps

## Installation

No external dependencies required. Uses Python standard library only.

```bash
# Clone or download the project
cd expense-tracker

# Run the application
python expense_tracker.py
```

**Requirements:** Python 3.6+

## Usage

### Interactive Mode

Run the application to access the interactive menu:

```bash
python expense_tracker.py
```

```
=== Expense Tracker ===
1. Add Expense
2. View All Expenses
3. View Total Spending
4. Save & Exit
5. Exit without Saving

Select an option (1-5):
```

### Programmatic Usage

```python
from expense_tracker import ExpenseTracker

# Initialize tracker (loads existing data if available)
tracker = ExpenseTracker("my_expenses.json")

# Add expenses
tracker.add_expense(25.50, "Food", "Lunch at restaurant")
tracker.add_expense(45.00, "Transport", "Uber to airport")
tracker.add_expense(12.99, "Entertainment", "Movie ticket")

# View all expenses
tracker.view_expenses()

# Get total spending
total = tracker.get_total()  # Returns 83.49

# Save to file
tracker.save_to_file()
```

## API Reference

### Class: ExpenseTracker

#### `__init__(data_file="expenses.json")`

Initialize the expense tracker with a data file.

**Parameters:**
- `data_file` (str): Path to the JSON file for storing expenses. Defaults to "expenses.json".

#### `add_expense(amount, category, description)`

Add a new expense to the tracker.

**Parameters:**
- `amount` (float): The expense amount in dollars
- `category` (str): Category of the expense (e.g., "Food", "Transport")
- `description` (str): Brief description of the expense

#### `view_expenses()`

Display all recorded expenses in a formatted table showing ID, date, category, amount, and description.

#### `get_total()`

Calculate and display the total of all expenses.

**Returns:**
- `float`: The sum of all expense amounts

#### `save_to_file()`

Save all expenses to the JSON data file.

#### `load_from_file()`

Load expenses from the JSON data file. Called automatically on initialization.

### Function: get_float_input(prompt)

Prompt user for a positive float value with validation.

**Parameters:**
- `prompt` (str): The input prompt to display

**Returns:**
- `float`: A validated positive number from user input

## Data Format

Expenses are stored in JSON format:

```json
{
  "next_id": 4,
  "expenses": [
    {
      "id": 1,
      "amount": 25.50,
      "category": "Food",
      "description": "Lunch at restaurant",
      "date": "2025-01-31 12:30"
    },
    {
      "id": 2,
      "amount": 45.00,
      "category": "Transport",
      "description": "Uber to airport",
      "date": "2025-01-31 14:15"
    }
  ]
}
```

## Project Structure

```
expense-tracker/
├── expense_tracker.py    # Main application
├── expenses.json         # Data storage (created on first save)
├── README.md             # This file
└── commands/             # Claude Code slash commands
    └── expense-tracker-doc.md
```

## License

MIT License
