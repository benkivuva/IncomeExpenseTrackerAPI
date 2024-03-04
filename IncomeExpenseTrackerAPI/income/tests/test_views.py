from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Income

User = get_user_model()

class IncomeListAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_income(self):
        url = reverse('incomes')
        data = {
            'description': 'Test Income',
            'amount': 100,
            'source': 'SALARY',
            'date': '2024-02-29'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_income_list(self):
        url = reverse('incomes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

class IncomeDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.income = Income.objects.create(description='Test Income', amount=100, source='SALARY', date='2024-02-29', owner=self.user)
        self.url = reverse('income', kwargs={'id': self.income.pk})

    def test_retrieve_income(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_income(self):
        data = {
            'description': 'Updated Income',
            'amount': 200,
            'source': 'SALARY',
            'date': '2024-03-01'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_income(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)