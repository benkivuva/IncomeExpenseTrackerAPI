from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Expense

User = get_user_model()

class ExpenseListAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_expense(self):
        url = reverse('expenses')
        data = {
            'description': 'Test Expense',
            'amount': 100,
            'category': 'FOOD',
            'date': '2024-02-29'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expense_list(self):
        url = reverse('expenses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

class ExpenseDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.expense = Expense.objects.create(description='Test Expense', amount=100, category='FOOD', date='2024-02-29', owner=self.user)
        self.url = reverse('expense', kwargs={'id': self.expense.pk})

    def test_retrieve_expense(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_expense(self):
        data = {
            'description': 'Updated Expense',
            'amount': 200,
            'category': 'TRAVEL',
            'date': '2024-03-01'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_expense(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)