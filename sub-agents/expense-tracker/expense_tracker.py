#!/usr/bin/env python3
"""
Expense Tracker - A simple command-line expense tracking application.

This module provides functionality to track personal expenses with categories,
persist data to JSON files, and view spending summaries.

Example:
    Run the application directly:

        $ python expense_tracker.py

    Or import and use programmatically:

        >>> from expense_tracker import ExpenseTracker
        >>> tracker = ExpenseTracker("my_expenses.json")
        >>> tracker.add_expense(25.50, "Food", "Lunch at cafe")
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


# Display constants
TABLE_WIDTH = 70
CURRENCY_SYMBOL = "$"
DATE_FORMAT = "%Y-%m-%d %H:%M"

# Menu options
MENU_ADD = "1"
MENU_VIEW = "2"
MENU_TOTAL = "3"
MENU_BY_CATEGORY = "4"
MENU_DELETE = "5"
MENU_SAVE_EXIT = "6"
MENU_EXIT = "7"


@dataclass
class Expense:
    """
    Represents a single expense record.

    Attributes:
        id: Unique identifier for the expense.
        amount: The expense amount (must be positive).
        category: Category of the expense (e.g., "Food", "Transport").
        description: Brief description of the expense.
        date: Timestamp when the expense was created.
    """

    id: int
    amount: float
    category: str
    description: str
    date: str

    @classmethod
    def create(
        cls, expense_id: int, amount: float, category: str, description: str
    ) -> Expense:
        """
        Factory method to create a new expense with current timestamp.

        Args:
            expense_id: Unique identifier for the expense.
            amount: The expense amount.
            category: Category of the expense.
            description: Brief description.

        Returns:
            A new Expense instance with current timestamp.
        """
        return cls(
            id=expense_id,
            amount=amount,
            category=category,
            description=description,
            date=datetime.now().strftime(DATE_FORMAT),
        )

    def to_dict(self) -> dict:
        """Convert expense to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> Expense:
        """Create an Expense from a dictionary."""
        return cls(**data)


class ExpenseTracker:
    """
    A simple expense tracking application that stores expenses in JSON format.

    This class provides methods to add, view, delete, and persist expense records.
    Each expense includes an amount, category, description, and timestamp.

    Attributes:
        data_file: Path to the JSON file for persistent storage.
        expenses: List of Expense objects.
        next_id: Auto-incrementing ID for new expenses.

    Example:
        >>> tracker = ExpenseTracker()
        >>> tracker.add_expense(50.00, "Transport", "Uber to airport")
        >>> tracker.get_total()
        50.0
    """

    def __init__(self, data_file: str = "expenses.json") -> None:
        """
        Initialize the ExpenseTracker with a data file.

        Args:
            data_file: Path to the JSON file for storing expenses.
                Defaults to "expenses.json" in the current directory.
        """
        self.data_file = data_file
        self.expenses: list[Expense] = []
        self.next_id = 1
        self.load_from_file()

    def add_expense(self, amount: float, category: str, description: str) -> Expense:
        """
        Add a new expense to the tracker.

        Args:
            amount: The expense amount in dollars (must be positive).
            category: Category of the expense (e.g., "Food", "Transport").
            description: Brief description of the expense.

        Returns:
            The newly created Expense object.

        Example:
            >>> tracker.add_expense(15.99, "Food", "Pizza delivery")
            Expense added successfully! (ID: 1)
        """
        expense = Expense.create(self.next_id, amount, category, description)
        self.expenses.append(expense)
        self.next_id += 1
        print(f"\nExpense added successfully! (ID: {expense.id})")
        return expense

    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by its ID.

        Args:
            expense_id: The ID of the expense to delete.

        Returns:
            True if expense was found and deleted, False otherwise.
        """
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                deleted = self.expenses.pop(i)
                print(f"\nDeleted expense: {deleted.description} ({CURRENCY_SYMBOL}{deleted.amount:.2f})")
                return True
        print(f"\nExpense with ID {expense_id} not found.")
        return False

    def find_expense(self, expense_id: int) -> Optional[Expense]:
        """
        Find an expense by its ID.

        Args:
            expense_id: The ID of the expense to find.

        Returns:
            The Expense if found, None otherwise.
        """
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None

    def view_expenses(self) -> None:
        """
        Display all recorded expenses in a formatted table.

        Prints a table showing ID, date, category, amount, and description
        for each expense. If no expenses exist, displays a message indicating
        no expenses have been recorded.
        """
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        self._print_expense_table(self.expenses)

    def view_by_category(self) -> None:
        """Display expenses grouped by category with subtotals."""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        categories: dict[str, list[Expense]] = {}
        for expense in self.expenses:
            if expense.category not in categories:
                categories[expense.category] = []
            categories[expense.category].append(expense)

        for category, expenses in sorted(categories.items()):
            subtotal = sum(exp.amount for exp in expenses)
            print(f"\n--- {category} (Subtotal: {CURRENCY_SYMBOL}{subtotal:.2f}) ---")
            self._print_expense_table(expenses, show_category=False)

    def _print_expense_table(
        self, expenses: list[Expense], show_category: bool = True
    ) -> None:
        """
        Print a formatted table of expenses.

        Args:
            expenses: List of expenses to display.
            show_category: Whether to include the category column.
        """
        print("\n" + "=" * TABLE_WIDTH)
        if show_category:
            print(
                f"{'ID':<5} {'Date':<18} {'Category':<12} {'Amount':>10}   {'Description'}"
            )
        else:
            print(f"{'ID':<5} {'Date':<18} {'Amount':>10}   {'Description'}")
        print("=" * TABLE_WIDTH)

        for exp in expenses:
            if show_category:
                print(
                    f"{exp.id:<5} {exp.date:<18} {exp.category:<12} "
                    f"{CURRENCY_SYMBOL}{exp.amount:>9.2f}   {exp.description}"
                )
            else:
                print(
                    f"{exp.id:<5} {exp.date:<18} "
                    f"{CURRENCY_SYMBOL}{exp.amount:>9.2f}   {exp.description}"
                )
        print("=" * TABLE_WIDTH)

    def get_total(self) -> float:
        """
        Calculate and display the total of all expenses.

        Returns:
            The sum of all expense amounts.

        Example:
            >>> tracker.add_expense(10.00, "Food", "Coffee")
            >>> tracker.add_expense(20.00, "Food", "Lunch")
            >>> tracker.get_total()
            Total Spending: $30.00
            30.0
        """
        total = sum(exp.amount for exp in self.expenses)
        print(f"\nTotal Spending: {CURRENCY_SYMBOL}{total:.2f}")
        return total

    def save_to_file(self) -> None:
        """
        Save all expenses to the JSON data file.

        Persists the current expenses list and next_id counter to the
        configured data file in JSON format.
        """
        data = {
            "next_id": self.next_id,
            "expenses": [exp.to_dict() for exp in self.expenses],
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nData saved to {self.data_file}")

    def load_from_file(self) -> None:
        """
        Load expenses from the JSON data file.

        Reads the configured data file and populates the expenses list
        and next_id counter. If the file doesn't exist, starts with
        empty expenses.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.expenses = [
                    Expense.from_dict(exp) for exp in data.get("expenses", [])
                ]
                self.next_id = data.get("next_id", 1)
            print(f"Loaded {len(self.expenses)} expense(s) from {self.data_file}")


def get_float_input(prompt: str) -> float:
    """
    Prompt user for a positive float value with validation.

    Args:
        prompt: The input prompt to display to the user.

    Returns:
        A validated positive number from user input.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int_input(prompt: str) -> int:
    """
    Prompt user for a positive integer value with validation.

    Args:
        prompt: The input prompt to display to the user.

    Returns:
        A validated positive integer from user input.
    """
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Expense Tracker ===")
    print(f"{MENU_ADD}. Add Expense")
    print(f"{MENU_VIEW}. View All Expenses")
    print(f"{MENU_TOTAL}. View Total Spending")
    print(f"{MENU_BY_CATEGORY}. View by Category")
    print(f"{MENU_DELETE}. Delete Expense")
    print(f"{MENU_SAVE_EXIT}. Save & Exit")
    print(f"{MENU_EXIT}. Exit without Saving")


def handle_add_expense(tracker: ExpenseTracker) -> None:
    """Handle the add expense menu action."""
    amount = get_float_input(f"Enter amount: {CURRENCY_SYMBOL}")
    category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
    description = input("Enter description: ").strip()
    tracker.add_expense(amount, category, description)


def handle_delete_expense(tracker: ExpenseTracker) -> None:
    """Handle the delete expense menu action."""
    if not tracker.expenses:
        print("\nNo expenses to delete.")
        return
    tracker.view_expenses()
    expense_id = get_int_input("Enter expense ID to delete: ")
    tracker.delete_expense(expense_id)


def handle_exit_without_save() -> bool:
    """
    Handle exit without save confirmation.

    Returns:
        True if user confirmed exit, False otherwise.
    """
    confirm = input("Are you sure? Unsaved changes will be lost. (y/n): ").strip().lower()
    return confirm == "y"


def main() -> None:
    """
    Main entry point for the Expense Tracker CLI application.

    Provides an interactive menu-driven interface for:
    - Adding new expenses
    - Viewing all recorded expenses
    - Viewing total spending
    - Viewing expenses by category
    - Deleting expenses
    - Saving data and exiting
    - Exiting without saving
    """
    tracker = ExpenseTracker()

    menu_handlers = {
        MENU_ADD: lambda: handle_add_expense(tracker),
        MENU_VIEW: tracker.view_expenses,
        MENU_TOTAL: tracker.get_total,
        MENU_BY_CATEGORY: tracker.view_by_category,
        MENU_DELETE: lambda: handle_delete_expense(tracker),
    }

    while True:
        display_menu()
        choice = input("\nSelect an option (1-7): ").strip()

        if choice in menu_handlers:
            menu_handlers[choice]()

        elif choice == MENU_SAVE_EXIT:
            tracker.save_to_file()
            print("Goodbye!")
            break

        elif choice == MENU_EXIT:
            if handle_exit_without_save():
                print("Goodbye!")
                break

        else:
            print("Invalid option. Please select 1-7.")


if __name__ == "__main__":
    main()
