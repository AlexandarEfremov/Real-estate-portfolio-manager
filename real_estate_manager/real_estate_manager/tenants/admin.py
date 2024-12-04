from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'property', 'monthly_rent', 'lease_start_date', 'lease_end_date')
    search_fields = ('first_name', 'last_name', 'property__name')
    list_filter = ('property', 'lease_start_date', 'lease_end_date')
