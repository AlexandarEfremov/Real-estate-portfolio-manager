from django.urls import path
from .views import ListTenantsView, TenantDetailView, TenantEditView, TenantDeleteView, CreateTenantView

urlpatterns = [
    path('', ListTenantsView.as_view(), name='list_tenants'),
    path('create/', CreateTenantView.as_view(), name='create_tenant'),
    path('<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    path('edit/<int:pk>/', TenantEditView.as_view(), name='tenant_edit'),
    path('delete/<int:pk>/', TenantDeleteView.as_view(), name='tenant_delete'),
]
