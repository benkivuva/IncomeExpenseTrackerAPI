from django.test import TestCase
from ..models import Expense
from ..serializers import ExpensesSerializer

class ExpensesSerializerTest(TestCase):
    def test_expenses_serializer_valid_data(self):
        """
        Test whether the ExpensesSerializer serializes data correctly.
        """
        expense_data = {
            'description': 'Test Expense',
            'amount': 100,
            'category': 'FOOD',
            'date': '2024-02-29'
        }
        serializer = ExpensesSerializer(data=expense_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertEqual(serialized_data['description'], expense_data['description'])
        self.assertEqual(serialized_data['amount'], expense_data['amount'])
        self.assertEqual(serialized_data['category'], expense_data['category'])
        self.assertEqual(serialized_data['date'], expense_data['date'])

    def test_expenses_serializer_invalid_data(self):
        """
        Test whether the ExpensesSerializer correctly identifies invalid data.
        """
        expense_data = {
            'description': 'Test Expense',
            'amount': -100,  # Negative amount, which is invalid
            'category': 'FOOD',
            'date': '2024-02-29'
        }
        serializer = ExpensesSerializer(data=expense_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)  # Check if 'amount' field is in errors

    def test_expenses_serializer_missing_fields(self):
        """
        Test whether the ExpensesSerializer correctly identifies missing fields.
        """
        expense_data = {
            'description': 'Test Expense',
            'category': 'FOOD',
            'date': '2024-02-29'
        }
        serializer = ExpensesSerializer(data=expense_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)  # Check if 'amount' field is in errors

    def test_expenses_serializer_extra_fields(self):
        """
        Test whether the ExpensesSerializer ignores extra fields.
        """
        expense_data = {
            'description': 'Test Expense',
            'amount': 100,
            'category': 'FOOD',
            'date': '2024-02-29',
            'extra_field': 'Extra Value'
        }
        serializer = ExpensesSerializer(data=expense_data)
        self.assertTrue(serializer.is_valid())