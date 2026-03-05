```python
import json
import re
from datetime import datetime
from typing import List, Dict, Optional

class ExpenseTracker:
    def __init__(self, filename: str = "expenses.json"):
        self.filename = filename
        self.expenses: List[Dict] = []
        self.load()

    def _validate_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    def _validate_amount(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        return float(amount)

    def add_expense(self, date: str, category: str, amount: float, note: str = "") -> None:
        try:
            date_obj = self._validate_date(date)
            amount = self._validate_amount(amount)
            if not category.strip():
                raise ValueError("Category cannot be empty.")

            expense = {
                "date": date_obj.isoformat(),
                "category": category.strip(),
                "amount": amount,
                "note": note.strip() if note else ""
            }
            self.expenses.append(expense)
            self.save()
        except ValueError as e:
            raise ValueError(f"Invalid input: {e}")

    def total_by_category(self) -> Dict[str, float]:
        totals = {}
        for expense in self.expenses:
            category = expense["category"]
            totals[category] = totals.get(category, 0) + expense["amount"]
        return totals

    def total_in_range(self, start_date: str, end_date: str) -> float:
        try:
            start = self._validate_date(start_date)
            end = self._validate_date(end_date)
            if start > end:
                raise ValueError("Start date must be before end date.")

            total = 0.0
            for expense in self.expenses:
                expense_date = datetime.strptime(expense["date"], "%Y-%m-%d").date()
                if start <= expense_date <= end:
                    total += expense["amount"]
            return total
        except ValueError as e:
            raise ValueError(f"Invalid date range: {e}")

    def save(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.expenses, f, indent=2)

    def load(self) -> None:
        try:
            with open(self.filename, "r") as f:
                self.expenses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.expenses = []

def display_menu():
    print("\nExpense Tracker Menu:")
    print("1. Add Expense")
    print("2. View Total by Category")
    print("3. View Total in Date Range")
    print("4. Exit")

def main():
    tracker = ExpenseTracker()
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            try:
                date = input("Enter date (YYYY-MM-DD): ").strip()
                category = input("Enter category: ").strip()
                amount = float(input("Enter amount: ").strip())
                note = input("Enter note (optional): ").strip()
                tracker.add_expense(date, category, amount, note)
                print("Expense added successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            totals = tracker.total_by_category()
            print("\nTotal by Category:")
            for category, total in totals.items():
                print(f"{category}: {total:.2f}")

        elif choice == "3":
            try:
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                total = tracker.total_in_range(start_date, end_date)
                print(f"Total in range: {total:.2f}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

import unittest

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker("test_expenses.json")
        self.tracker.expenses = []  # Clear existing data

    def test_add_valid_expense(self):
        self.tracker.add_expense("2023-01-01", "Food", 10.50)
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0]["category"], "Food")

    def test_add_invalid_date(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("2023/01/01", "Food", 10.50)

    def test_add_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("2023-01-01", "Food", -10.50)

    def test_add_empty_category(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense("2023-01-01", "", 10.50)

    def test_total_by_category(self):
        self.tracker.add_expense("2023-01-01", "Food", 10.50)
        self.tracker.add_expense("2023-01-02", "Food", 5.25)
        self.tracker.add_expense("2023-01-03", "Transport", 15.00)
        totals = self.tracker.total_by_category()
        self.assertEqual(totals["Food"], 15.75)
        self.assertEqual(totals["Transport"], 15.00)

    def test_total_in_range(self):
        self.tracker.add_expense("2023-01-01", "Food", 10.50)
        self.tracker.add_expense("2023-01-02", "Food", 5.25)
        self.tracker.add_expense("2023-01-03", "Transport", 15.00)
        total = self.tracker.total_in_range("2023-01-01", "2023-01-02")
        self.assertEqual(total, 15.75)

    def test_total_in_range_invalid_dates(self):
        with self.assertRaises(ValueError):
            self.tracker.total_in_range("2023-01-03", "2023-01-01")

    def test_total_in_range_empty_range(self):
        total = self.tracker.total_in_range("2023-01-01", "2023-01-01")
        self.assertEqual(total, 0.0)

    def test_save_and_load(self):
        self.tracker.add_expense("2023-01-01", "Food", 10.50)
        self.tracker.save()
        new_tracker = ExpenseTracker("test_expenses.json")
        self.assertEqual(len(new_tracker.expenses), 1)
        self.assertEqual(new_tracker.expenses[0]["amount"], 10.50)

    def test_load_empty_file(self):
        new_tracker = ExpenseTracker("nonexistent_file.json")
        self.assertEqual(len(new_tracker.expenses), 0)

    def test_note_handling(self):
        self.tracker.add_expense("2023-01-01", "Food", 10.50, "Grocery")
        self.assertEqual(self.tracker.expenses[0]["note"], "Grocery")

    def test_note_empty(self):
        self.tracker.add_expense("2023-01-01", "Food", 10.50)
        self.assertEqual(self.tracker.expenses[0]["note"], "")

if __name__ == "__main__":
    unittest.main()
```

