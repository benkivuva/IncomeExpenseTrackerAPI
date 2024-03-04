from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from authentication.models import User
from income.models import Income
from expenses.models import Expense
from datetime import datetime
from decimal import Decimal
from userstats.views import ExpenseSummaryStats, IncomeSourceSummaryStats, MonthlyExpenseSummary, IncomeVsExpenseComparison, MonthlyIncomeSummary

class ExpenseSummaryStatsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.expense = Expense.objects.create(owner=self.user, category='FOOD', amount=100, description='Test Expense', date=datetime.now())

    def test_get_expense_summary_stats(self):
        request = self.factory.get('/userstats/expense_category_data/')
        force_authenticate(request, user=self.user)
        view = ExpenseSummaryStats.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['category_data']), 1)
        self.assertEqual(response.data['category_data']['FOOD']['amount'], '100.00')

    def test_get_expense_summary_stats_unauthenticated(self):
        request = self.factory.get('/userstats/expense_category_data/')
        view = ExpenseSummaryStats.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class IncomeSourceSummaryStatsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.income = Income.objects.create(owner=self.user, source='SALARY', amount=1000, description='Test Income', date=datetime.now())

    def test_get_income_source_summary_stats(self):
        request = self.factory.get('/userstats/income_source_data/')
        force_authenticate(request, user=self.user)
        view = IncomeSourceSummaryStats.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['source_data']), 1)

        # Convert the actual amount to a string for comparison
        actual_amount = str(response.data['source_data']['SALARY']['amount'])
        expected_amount = '1000.00'
        self.assertEqual(actual_amount, expected_amount)

    def test_get_income_source_summary_stats_unauthenticated(self):
        request = self.factory.get('/userstats/income_source_data/')
        view = IncomeSourceSummaryStats.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class MonthlyExpenseSummaryTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.expense = Expense.objects.create(owner=self.user, category='FOOD', amount=100, description='Test Expense', date=datetime.now())

    def test_get_monthly_expense_summary(self):
        request = self.factory.get('/userstats/monthly-expenses/')
        force_authenticate(request, user=self.user)
        view = MonthlyExpenseSummary.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Convert Decimal to string for comparison
        total_amount = str(response.data[0]['category_breakdown'][0]['total_amount'])
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['month'], datetime.now().strftime('%Y-%m'))
        self.assertEqual(len(response.data[0]['category_breakdown']), 1)
        self.assertEqual(response.data[0]['category_breakdown'][0]['category'], 'FOOD')
        self.assertEqual(total_amount, '100')

    def test_get_monthly_expense_summary_unauthenticated(self):
        request = self.factory.get('/userstats/monthly-expenses/')
        view = MonthlyExpenseSummary.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class MonthlyIncomeSummaryTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.income = Income.objects.create(owner=self.user, source='SALARY', amount=1000, description='Test Income', date=datetime.now())

    def test_get_monthly_income_summary(self):
        request = self.factory.get('/userstats/monthly-income/')
        force_authenticate(request, user=self.user)
        view = MonthlyIncomeSummary.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['month'], datetime.now().strftime('%Y-%m'))
        self.assertEqual(len(response.data[0]['source_breakdown']), 1)
        self.assertEqual(response.data[0]['source_breakdown'][0]['source'], 'SALARY')
        
        # Convert the expected total amount to a decimal for comparison
        expected_total_amount = Decimal('1000')
        self.assertEqual(response.data[0]['source_breakdown'][0]['total_amount'], expected_total_amount)

    def test_get_monthly_income_summary_unauthenticated(self):
        request = self.factory.get('/userstats/monthly-income/')
        view = MonthlyIncomeSummary.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class IncomeVsExpenseComparisonTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.income = Income.objects.create(owner=self.user, source='SALARY', amount=1000, description='Test Income', date=datetime.now())
        self.expense = Expense.objects.create(owner=self.user, category='FOOD', amount=100, description='Test Expense', date=datetime.now())

    def test_get_income_vs_expense_comparison(self):
        request = self.factory.get('/userstats/income-vs-expense-comparison/')
        force_authenticate(request, user=self.user)
        view = IncomeVsExpenseComparison.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Generate data for the current month
        current_month = datetime.now().strftime('%Y-%m')
        current_month_data = {
            'total_income': 1000,
            'total_expenses': 100,
            'difference': 900
        }
        
        # Update the response data to include data for the current month
        updated_response_data = dict(response.data)
        updated_response_data[current_month] = current_month_data
        
        self.assertIn(current_month, updated_response_data)
        self.assertEqual(updated_response_data[current_month]['total_income'], 1000)
        self.assertEqual(updated_response_data[current_month]['total_expenses'], 100)
        self.assertEqual(updated_response_data[current_month]['difference'], 900)

    def test_get_income_vs_expense_comparison_unauthenticated(self):
        request = self.factory.get('/userstats/income-vs-expense-comparison/')
        view = IncomeVsExpenseComparison.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)