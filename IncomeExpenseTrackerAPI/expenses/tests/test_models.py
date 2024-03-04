from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Expense

User = get_user_model()

class ExpenseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create an expense for testing
        cls.expense = Expense.objects.create(
            category='FOOD',
            amount=100.00,
            description='Test expense description',
            owner=cls.user,
            date='2024-02-29'
        )

    def test_category_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        category_label = expense._meta.get_field('category').verbose_name
        self.assertEqual(category_label, 'category')

    def test_amount_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(expense.amount, 100.00)

    def test_description_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(expense.description, 'Test expense description')

    def test_owner_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(expense.owner, self.user)

    def test_date_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(str(expense.date), '2024-02-29')

    def test_created_at_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertIsNotNone(expense.created_at)

    def test_updated_at_field(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertIsNotNone(expense.updated_at)

    def test_ordering(self):
        self.assertEqual(Expense._meta.ordering, ['-updated_at'])

    def test_str_method(self):
        expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(str(expense), f"{self.user}'s income")