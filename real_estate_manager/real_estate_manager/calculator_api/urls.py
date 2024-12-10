from django.urls import path
from .views import InvestmentCalculatorView, ROICalculatorPageView

urlpatterns = [
    path('investment-calculator-api/', InvestmentCalculatorView.as_view(), name='investment-calculator-api'),
    path('investment-calculator/', ROICalculatorPageView.as_view(), name='investment-calculator'),
]
