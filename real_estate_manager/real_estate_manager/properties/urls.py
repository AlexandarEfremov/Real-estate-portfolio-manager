# properties/urls.py
from django.urls import path
from .views import PropertyListView, PropertyCreateView, PropertyUpdateView, PropertyDeleteView, PropertyDetailView

urlpatterns = [
    path('', PropertyListView.as_view(), name='list_properties'),
    path('create/', PropertyCreateView.as_view(), name='create_property'),
    path('<int:pk>/edit/', PropertyUpdateView.as_view(), name='update_property'),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='delete_property'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),  # Add this line for the property detail view
]
