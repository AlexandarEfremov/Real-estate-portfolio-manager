from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Income URLs
    path('income/', views.IncomeListView.as_view(), name='income_list'),
    path('income/create/', views.IncomeCreateUpdateView.as_view(), name='create_income'),
    path('income/<int:income_id>/update/', views.IncomeCreateUpdateView.as_view(), name='update_income'),
    path('income/<int:pk>/delete/', views.IncomeDeleteView.as_view(), name='delete_income'),

    # Expense URLs
    path('expense/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expense/create/', views.ExpenseCreateUpdateView.as_view(), name='create_expense'),
    path('expense/<int:expense_id>/update/', views.ExpenseCreateUpdateView.as_view(), name='update_expense'),
    path('expense/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expense/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='delete_expense'),
]
