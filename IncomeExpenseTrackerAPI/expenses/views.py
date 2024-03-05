from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ExpensesSerializer
from .models import Expense
from rest_framework import permissions
from .permissions import IsOwner


class ExpenseListAPIView(ListCreateAPIView):
    """
    View for listing and creating expenses.

    This view allows authenticated users to list their expenses and create new expense entries.
    """
    serializer_class = ExpensesSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual expenses.

    This view allows authenticated users who are the owners of the expense to retrieve, update,
    and delete their own expense records.
    """
    serializer_class = ExpensesSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Expense.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)