from rest_framework import serializers


class InvestmentCalculatorSerializer(serializers.Serializer):
    purchase_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_rent = serializers.DecimalField(max_digits=10, decimal_places=2)
    annual_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)

    def calculate_roi(self):
        data = self.validated_data
        purchase_price = data['purchase_price']
        monthly_rent = data['monthly_rent']
        annual_expenses = data['annual_expenses']

        annual_income = monthly_rent * 12

        roi = (annual_income - annual_expenses) / purchase_price * 100
        return roi
