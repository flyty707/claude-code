#!/usr/bin/env python3
import json
import os
from datetime import datetime


class ExpenseTracker:
    def __init__(self, data_file="expenses.json"):
        self.data_file = data_file
        self.expenses = []
        self.next_id = 1
        self.load_from_file()

    def add_expense(self, amount, category, description):
        expense = {
            "id": self.next_id,
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.expenses.append(expense)
        self.next_id += 1
        print(f"\nExpense added successfully! (ID: {expense['id']})")

    def view_expenses(self):
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<5} {'Date':<18} {'Category':<12} {'Amount':>10}   {'Description'}")
        print("=" * 70)
        for exp in self.expenses:
            print(
                f"{exp['id']:<5} {exp['date']:<18} {exp['category']:<12} "
                f"${exp['amount']:>9.2f}   {exp['description']}"
            )
        print("=" * 70)

    def get_total(self):
        total = sum(exp["amount"] for exp in self.expenses)
        print(f"\nTotal Spending: ${total:.2f}")
        return total

    def save_to_file(self):
        data = {"next_id": self.next_id, "expenses": self.expenses}
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\nData saved to {self.data_file}")

    def load_from_file(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.expenses = data.get("expenses", [])
                self.next_id = data.get("next_id", 1)
            print(f"Loaded {len(self.expenses)} expense(s) from {self.data_file}")


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Spending")
        print("4. Save & Exit")
        print("5. Exit without Saving")

        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            amount = get_float_input("Enter amount: $")
            category = input("Enter category (e.g., Food, Transport, Entertainment): ").strip()
            description = input("Enter description: ").strip()
            tracker.add_expense(amount, category, description)

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            tracker.get_total()

        elif choice == "4":
            tracker.save_to_file()
            print("Goodbye!")
            break

        elif choice == "5":
            confirm = input("Are you sure? Unsaved changes will be lost. (y/n): ").strip().lower()
            if confirm == "y":
                print("Goodbye!")
                break

        else:
            print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
