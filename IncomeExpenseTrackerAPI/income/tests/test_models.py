from django.test import TestCase
from authentication.models import User
from ..models import Income

class IncomeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def setUp(self):
        # Set up modified objects used by test methods
        self.income = Income.objects.create(
            source='SALARY', amount=100, description='Test Income', owner=self.user, date='2024-02-29')

    def test_str_representation(self):
        expected_str = f"{self.user}s income"
        actual_str = str(self.income)
        self.assertIn(expected_str, actual_str)


    def test_ordering(self):
        income_list = Income.objects.all()
        self.assertGreater(len(income_list), 0)
        self.assertEqual(income_list.first(), self.income)

    def test_date_field(self):
        self.assertEqual(self.income.date, '2024-02-29')

    def test_owner_field(self):
        self.assertEqual(self.income.owner, self.user)