import json
from datetime import datetime
from typing import List, Dict

class ExpenseTracker:
    def __init__(self, filename: str = 'expenses.json'):
        self.filename = filename
        self.expenses: List[Dict] = []
        self.load()

    def add_expense(self, date: str, category: str, amount: float, note: str = '') -> None:
        if not self.is_valid_date(date):
            raise ValueError("Invalid date format, should be YYYY-MM-DD")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.expenses.append({'date': date, 'category': category, 'amount': amount, 'note': note})
        self.save()

    def total_by_category(self) -> Dict[str, float]:
        total = {}
        for expense in self.expenses:
            if expense['category'] in total:
                total[expense['category']] += expense['amount']
            else:
                total[expense['category']] = expense['amount']
        return total

    def total_in_range(self, start_date: str, end_date: str) -> float:
        if not self.is_valid_date(start_date) or not self.is_valid_date(end_date):
            raise ValueError("Invalid date format, should be YYYY-MM-DD")
        total = 0
        for expense in self.expenses:
            if start_date <= expense['date'] <= end_date:
                total += expense['amount']
        return total

    def save(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump(self.expenses, f)

    def load(self) -> None:
        try:
            with open(self.filename, 'r') as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker(filename='test_expenses.json')

    def tearDown(self):
        self.tracker.expenses = []
        self.tracker.save()

    def test_add_expense_valid(self):
        self.tracker.add_expense('2021-01-01', 'Food', 100)
        self.assertEqual(len(self.tracker.expenses), 1)

    def test_add_expense_invalid_date(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense('2021-01-32', 'Food', 100)

    def test_add_expense_non_positive_amount(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense('2021-01-01', 'Food', -100)

    def test_total_by_category(self):
        self.tracker.add_expense('2021-01-01', 'Food', 100)
        self.tracker.add_expense('2021-01-01', 'Transport', 50)
        self.assertEqual(self.tracker.total_by_category(), {'Food': 100, 'Transport': 50})

    def test_total_in_range(self):
        self.tracker.add_expense('2021-01-01', 'Food', 100)
        self.tracker.add_expense('2021-01-02', 'Transport', 50)
        self.assertEqual(self.tracker.total_in_range('2021-01-01', '2021-01-02'), 150)

    def test_load_and_save(self):
        self.tracker.add_expense('2021-01-01', 'Food', 100)
        self.tracker.save()
        self.tracker.expenses = []
        self.tracker.load()
        self.assertEqual(len(self.tracker.expenses), 1)

if __name__ == '__main__':
    unittest.main()
