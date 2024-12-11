from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvestmentCalculatorSerializer

class InvestmentCalculatorView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize the input data
        serializer = InvestmentCalculatorSerializer(data=request.data)

        # Check if the input is valid
        if serializer.is_valid():
            # Calculate ROI and return the result
            roi = serializer.calculate_roi()
            return Response({'roi': roi}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ROICalculatorPageView(TemplateView):
    template_name = 'calculator_api/roi_calculator.html'

    def post(self, request, *args, **kwargs):
        purchase_price = request.POST.get('purchase_price')
        monthly_rent = request.POST.get('monthly_rent')
        annual_expenses = request.POST.get('annual_expenses')

        data = {
            "purchase_price": purchase_price,
            "monthly_rent": monthly_rent,
            "annual_expenses": annual_expenses,
        }

        serializer = InvestmentCalculatorSerializer(data=data)
        if serializer.is_valid():
            roi = serializer.calculate_roi()
            return render(request, self.template_name, {"roi": roi, "data": data})

        return render(request, self.template_name, {"errors": serializer.errors, "data": data})
