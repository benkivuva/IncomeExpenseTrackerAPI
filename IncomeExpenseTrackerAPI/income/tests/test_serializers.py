from rest_framework.test import APITestCase
from ..serializers import IncomeSerializer

class IncomeSerializerTest(APITestCase):
    def test_income_serializer_valid_data(self):
        valid_data = {
            'description': 'Test Income',
            'amount': 100,
            'source': 'SALARY',
            'date': '2024-02-29'
        }
        serializer = IncomeSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_income_serializer_invalid_data(self):
        invalid_data = {
            'description': 'Test Income',
            'amount': 'Invalid',  # amount should be a number
            'source': 'SALARY',
            'date': '2024-02-29'
        }
        serializer = IncomeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())