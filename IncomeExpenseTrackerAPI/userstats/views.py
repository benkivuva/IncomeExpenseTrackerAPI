from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import datetime
from expenses.models import Expense
from income.models import Income

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