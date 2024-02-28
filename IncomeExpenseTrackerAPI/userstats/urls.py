from django.urls import path
from .views import ExpenseSummaryStats, IncomeSourceSummaryStats, MonthlyExpenseSummary, IncomeVsExpenseComparison, MonthlyIncomeSummary

urlpatterns = [
    path('expense_category_data/', ExpenseSummaryStats.as_view(), name='expense-summary'),
    path('income_source_data/', IncomeSourceSummaryStats.as_view(), name='income-source-summary'),
    path('monthly-expenses/', MonthlyExpenseSummary.as_view(), name='monthly-expenses-summary'),
    path('monthly-income/', MonthlyIncomeSummary.as_view(), name='monthly-income-summary'),
    path('income-vs-expense-comparison/', IncomeVsExpenseComparison.as_view(), name='income-vs-expense-comparison'),
]