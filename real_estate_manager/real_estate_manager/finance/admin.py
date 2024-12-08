from django.contrib import admin
from .models import Income, Expense

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    # Update 'property' to 'tenant' in the list_display and list_filter
    list_display = ('amount', 'date', 'tenant', 'description')  # Replace 'property' with 'tenant'
    list_filter = ('date', 'tenant')  # Replace 'property' with 'tenant'
    search_fields = ('description', 'tenant__first_name', 'tenant__last_name')  # Update to search by tenant's name

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'property', 'category', 'description')
    list_filter = ('category', 'date', 'property')
    search_fields = ('description', 'property__name')
