from django.urls import path
from .views import ExpenseSummaryStats, IncomeSourceSummaryStats

urlpatterns = [
    path('expense_category_data/', ExpenseSummaryStats.as_view(), name='expense-summary'),
    path('income_source_data/', IncomeSourceSummaryStats.as_view(), name='income-source-summary'),
    # other URL patterns
]