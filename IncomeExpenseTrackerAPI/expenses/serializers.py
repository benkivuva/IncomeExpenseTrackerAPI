from rest_framework import serializers
from .models import Expense

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'date', 'description', 'amount', 'category']

    def validate_amount(self, value):
        """
        Validate that the amount is not negative.
        """
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value

    def to_representation(self, instance):
        """
        Convert the amount field to an integer if it's a string.
        """
        data = super().to_representation(instance)
        amount = data.get('amount')
        if isinstance(amount, str):
            try:
                data['amount'] = int(float(amount))
            except ValueError:
                # Handle the case where amount cannot be converted to float or int
                pass
        return data