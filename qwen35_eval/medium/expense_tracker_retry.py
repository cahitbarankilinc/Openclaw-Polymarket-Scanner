import json
import os
import unittest
from datetime import datetime
from typing import List, Dict, Optional

class ExpenseTracker:
    def __init__(self, file_path: str = "expenses.json"):
        self.file_path = file_path
        self.expenses: List[Dict] = []
        self.load_data()

    def load_data(self):
        """Load expenses from JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
            except (json.JSONDecodeError, IOError):
                self.expenses = []

    def save_data(self):
        """Save expenses to JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump({'expenses': self.expenses}, f)
        except IOError:
            print("Error saving data.")

    def add_expense(self, date: str, category: str, amount: float, note: str = '') -> bool:
        """
        Add an expense with strict validation.
        Returns True if successful, False otherwise.
        """
        # Validate Date (YYYY-MM-DD)
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format '{date}'. Expected YYYY-MM-DD.")
            return False

        # Validate Amount (> 0)
        if amount <= 0:
            print(f"Invalid amount '{amount}'. Must be greater than 0.")
            return False

        # Add to list
        self.expenses.append({
            'date': date,
            'category': category,
            'amount': amount,
            'note': note
        })
        
        # Persist immediately on add (optional design choice for CLI responsiveness)
        self.save_data()
        return True

    def total_by_category(self) -> Dict[str, float]:
        """Calculate total expenses grouped by category."""
        totals = {}
        for expense in self.expenses:
            cat = expense['category']
            if cat in totals:
                totals[cat] += expense['amount']
            else:
                totals[cat] = expense['amount']
        return totals

    def total_in_range(self, start_date: str, end_date: str) -> float:
        """Calculate total expenses within a date range (inclusive)."""
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Expected YYYY-MM-DD.")
            return 0.0

        total = 0.0
        for expense in self.expenses:
            exp_dt = datetime.strptime(expense['date'], '%Y-%m-%d')
            if start_dt <= exp_dt <= end_dt:
                total += expense['amount']
        return total

    def save(self):
        """Explicitly save current state."""
        self.save_data()

    def load(self, file_path: str):
        """Load data from a specific file path."""
        self.file_path = file_path
        self.load_data()


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.test_file = "test_expenses.json"
        self.tracker = ExpenseTracker(self.test_file)
        # Clear initial data if any
        self.tracker.expenses = []

    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_expense_valid(self):
        """Test adding a valid expense."""
        result = self.tracker.add_expense("2023-10-05", "Food", 50.0, "Lunch")
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0]['amount'], 50.0)

    def test_add_expense_invalid_date_format(self):
        """Test adding expense with invalid date."""
        result = self.tracker.add_expense("05-10-2023", "Food", 50.0)
        self.assertFalse(result)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_add_expense_negative_amount(self):
        """Test adding expense with negative amount."""
        result = self.tracker.add_expense("2023-10-05", "Food", -50.0)
        self.assertFalse(result)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_add_expense_zero_amount(self):
        """Test adding expense with zero amount."""
        result = self.tracker.add_expense("2023-10-05", "Food", 0.0)
        self.assertFalse(result)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_total_by_category_single_item(self):
        """Test total by category with one item."""
        self.tracker.add_expense("2023-10-05", "Food", 50.0)
        totals = self.tracker.total_by_category()
        self.assertEqual(totals["Food"], 50.0)

    def test_total_by_category_multiple_items(self):
        """Test total by category with multiple items."""
        self.tracker.add_expense("2023-10-05", "Food", 50.0)
        self.tracker.add_expense("2023-10-06", "Food", 20.0)
        self.tracker.add_expense("2023-10-07", "Transport", 15.0)
        totals = self.tracker.total_by_category()
        self.assertEqual(totals["Food"], 70.0)
        self.assertEqual(totals["Transport"], 15.0)

    def test_total_in_range_single_item(self):
        """Test total in range with one item inside."""
        self.tracker.add_expense("2023-10-05", "Food", 50.0)
        total = self.tracker.total_in_range("2023-10-01", "2023-10-10")
        self.assertEqual(total, 50.0)

    def test_total_in_range_outside_items(self):
        """Test total in range with items outside."""
        self.tracker.add_expense("2023-10-05", "Food", 50.0)
        self.tracker.add_expense("2023-11-01", "Food", 100.0)
        total = self.tracker.total_in_range("2023-10-01", "2023-10-10")
        self.assertEqual(total, 50.0)

    def test_total_in_range_empty(self):
        """Test total in range with no items."""
        total = self.tracker.total_in_range("2023-01-01", "2023-12-31")
        self.assertEqual(total, 0.0)

    def test_save_and_load_persistence(self):
        """Test saving and loading data."""
        self.tracker.add_expense("2023-10-05", "Food", 50.0)
        self.tracker.save()
        
        # Reload from file
        new_tracker = ExpenseTracker(self.test_file)
        self.assertEqual(len(new_tracker.expenses), 1)
        self.assertEqual(new_tracker.expenses[0]['amount'], 50.0)

    def test_invalid_date_range_format(self):
        """Test total in range with invalid date format."""
        result = self.tracker.total_in_range("05-10-2023", "2023-10-10")
        self.assertEqual(result, 0.0)

    def test_add_expense_with_note(self):
        """Test adding expense with a note."""
        result = self.tracker.add_expense("2023-10-05", "Food", 50.0, "Important lunch")
        self.assertTrue(result)
        self.assertEqual(self.tracker.expenses[0]['note'], "Important lunch")

    def test_total_in_range_future_date(self):
        """Test total in range with future dates (should work if data exists)."""
        # Add a past date
        self.tracker.add_expense("2023-01-01", "Food", 50.0)
        # Query a range including the past date
        total = self.tracker.total_in_range("2023-01-01", "2023-12-31")
        self.assertEqual(total, 50.0)


if __name__ == '__main__':
    # Run CLI Menu if executed directly
    print("=== Expense Tracker CLI ===")
    while True:
        try:
            choice = input("\nSelect option (1-4): ").strip()
        except EOFError:
            break

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ").strip()
            category = input("Enter category: ").strip()
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            note = input("Enter note (optional): ").strip()
            if ExpenseTracker().add_expense(date, category, amount, note):
                print("Expense added successfully.")
        elif choice == '2':
            totals = ExpenseTracker().total_by_category()
            print("\nTotal by Category:")
            for cat, amt in totals.items():
                print(f"  {cat}: ${amt:.2f}")
        elif choice == '3':
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            total = ExpenseTracker().total_in_range(start_date, end_date)
            print(f"\nTotal in range: ${total:.2f}")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

    # Run Unit Tests
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        unittest.main()
