from django.urls import path
from . import views

app_name = 'finance'  # This should match the app_name used in the template

urlpatterns = [
    path('income/', views.IncomeListView.as_view(), name='income_list'),
    path('income/create/', views.IncomeCreateUpdateView.as_view(), name='create_income'),
    # Make sure the name is 'create_income'
    path('income/<int:income_id>/update/', views.IncomeCreateUpdateView.as_view(), name='update_income'),

    path('expense/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expense/create/', views.ExpenseCreateUpdateView.as_view(), name='create_expense'),
    # Make sure the name is 'create_expense'
    path('expense/<int:expense_id>/update/', views.ExpenseCreateUpdateView.as_view(), name='update_expense'),
]
