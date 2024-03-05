from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import IncomeSerializer
from .models import Income
from rest_framework import permissions
from .permissions import IsOwner


class IncomeListAPIView(ListCreateAPIView):
    """
    View for listing and creating income records.

    This view allows authenticated users to list their income records and create new income entries.
    """
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting individual income records.

    This view allows authenticated users who are the owners of the income record to retrieve, update,
    and delete their own income records.
    """
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Income.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)