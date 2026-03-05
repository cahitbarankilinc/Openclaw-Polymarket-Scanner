```python
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
        
        Args:
            date (str): Date in YYYY-MM-DD format.
            category (str): Expense category.
            amount (float): Amount (> 0).
            note (str): Optional note.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        # Validate date
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format '{date}'. Expected YYYY-MM-DD.")
            return False

        # Validate amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            print(f"Invalid amount '{amount}'. Must be a positive number.")
            return False

        expense = {
            'date': date,
            'category': category,
            'amount': amount,
            'note': note
        }
        self.expenses.append(expense)
        self.save_data()
        print(f"Expense added: ${amount:.2f} on {date} ({category})")
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
        """Calculate total expenses within a date range."""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format. Expected YYYY-MM-DD.")
            return 0.0

        total = 0.0
        for expense in self.expenses:
            exp_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            if start <= exp_date <= end:
                total += expense['amount']
        return total

    def get_expenses(self) -> List[Dict]:
        """Return a copy of the expenses list."""
        return self.expenses.copy()


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker("test_expenses.json")
        # Pre-populate with some data for testing ranges
        self.tracker.add_expense("2023-01-15", "Food", 50.0)
        self.tracker.add_expense("2023-01-20", "Transport", 20.0)
        self.tracker.add_expense("2023-02-10", "Food", 30.0)
        self.tracker.add_expense("2023-02-15", "Entertainment", 100.0)

    def tearDown(self):
        # Clean up test file
        if os.path.exists("test_expenses.json"):
            os.remove("test_expenses.json")

    def test_add_expense_valid(self):
        """Test adding a valid expense."""
        result = self.tracker.add_expense("2023-03-01", "Shopping", 15.5)
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.get_expenses()), 4)

    def test_add_expense_invalid_date_format(self):
        """Test adding expense with invalid date."""
        result = self.tracker.add_expense("01-01-2023", "Food", 10.0)
        self.assertFalse(result)

    def test_add_expense_negative_amount(self):
        """Test adding expense with negative amount."""
        result = self.tracker.add_expense("2023-04-01", "Food", -5.0)
        self.assertFalse(result)

    def test_add_expense_zero_amount(self):
        """Test adding expense with zero amount."""
        result = self.tracker.add_expense("2023-04-01", "Food", 0.0)
        self.assertFalse(result)

    def test_total_by_category_basic(self):
        """Test basic category total calculation."""
        totals = self.tracker.total_by_category()
        self.assertIn("Food", totals)
        self.assertEqual(totals["Food"], 80.0)

    def test_total_by_category_empty(self):
        """Test category total with no expenses."""
        tracker = ExpenseTracker("empty_test.json")
        tracker.save_data()
        totals = tracker.total_by_category()
        self.assertEqual(totals, {})

    def test_total_in_range_exact_match(self):
        """Test range sum matching exact dates."""
        total = self.tracker.total_in_range("2023-01-15", "2023-01-20")
        self.assertEqual(total, 70.0)

    def test_total_in_range_partial_match(self):
        """Test range sum including partial dates."""
        total = self.tracker.total_in_range("