from django.contrib import admin
from .models import Income, Expense

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'tenant', 'description')
    list_filter = ('date', 'tenant')
    search_fields = ('description', 'tenant__first_name', 'tenant__last_name')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'property', 'category', 'description')
    list_filter = ('category', 'date', 'property')
    search_fields = ('description', 'property__name')
