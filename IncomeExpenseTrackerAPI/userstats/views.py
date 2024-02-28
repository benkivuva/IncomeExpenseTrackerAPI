from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import datetime
from expenses.models import Expense
from income.models import Income
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth


class ExpenseSummaryStats(APIView):

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {'amount': str(amount)}

    def get_category(self, expense):
        return expense.category 

    def get(self, request):
        if not request.user.is_authenticated:  # Check if user is authenticated
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30*12)
        expenses = Expense.objects.filter(
            owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        
        final = {}
        categories = list(set(map(self.get_category, expenses)))
        for category in categories:
            final[category] = self.get_amount_for_category(expenses, category)
        
        # Include categories with zero expenses
        for category in categories:
            if category not in final:
                final[category] = {'amount': '0'}

        return Response({'category_data': final}, status=status.HTTP_200_OK)
    
class IncomeSourceSummaryStats(APIView):

    def get_amount_for_source(self, income_list, source):
        incomes = income_list.filter(source=source)
        amount = 0
        for income in incomes:
            amount += income.amount
        return {'amount': str(amount)}

    def get_source(self, income):
        return income.source 

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30*12)
        incomes = Income.objects.filter(
            owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        
        final = {}
        sources = list(set(map(self.get_source, incomes)))
        for source in sources:
            final[source] = self.get_amount_for_source(incomes, source)
        
        # Include sources with zero income
        for source in sources:
            if source not in final:
                final[source] = {'amount': '0'}

        return Response({'source_data': final}, status=status.HTTP_200_OK)
    
from django.db.models import Count, F

class MonthlyExpenseSummary(APIView):
    """
    Provides a summary of the user's expenses for each month,
    including the total amount spent, average daily expenditure,
    and breakdown of expenses by category.
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Query expenses grouped by month and category
        expense_summary = Expense.objects.filter(owner=request.user).annotate(
            month=TruncMonth('date')
        ).values('month', 'category').annotate(
            total_amount=Sum('amount')
        ).order_by('month', 'category')
        
        # Prepare response data
        response_data = []
        current_month = None
        month_data = None
        for item in expense_summary:
            if item['month'] != current_month:
                if month_data:
                    response_data.append(month_data)
                current_month = item['month']
                month_data = {
                    'month': current_month.strftime('%Y-%m'),
                    'category_breakdown': []
                }
            month_data['category_breakdown'].append({
                'category': item['category'],
                'total_amount': item['total_amount']
            })
        
        # Append the last month data
        if month_data:
            response_data.append(month_data)
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class MonthlyIncomeSummary(APIView):
    """
    Provides a summary of the user's income for each month,
    including the total amount earned and breakdown of income by source.
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Query income grouped by month and source
        income_summary = Income.objects.filter(owner=request.user).annotate(
            month=TruncMonth('date')
        ).values('month', 'source').annotate(
            total_amount=Sum('amount')
        ).order_by('month', 'source')
        
        # Prepare response data
        response_data = []
        current_month = None
        month_data = None
        for item in income_summary:
            if item['month'] != current_month:
                if month_data:
                    response_data.append(month_data)
                current_month = item['month']
                month_data = {
                    'month': current_month.strftime('%Y-%m'),
                    'source_breakdown': []
                }
            month_data['source_breakdown'].append({
                'source': item['source'],
                'total_amount': item['total_amount']
            })
        
        # Append the last month data
        if month_data:
            response_data.append(month_data)
        
        return Response(response_data, status=status.HTTP_200_OK)