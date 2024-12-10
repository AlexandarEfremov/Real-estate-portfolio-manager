from django.urls import path

from real_estate_manager.parking_api.views import ParkingSpaceListCreateAPIView, ParkingSpaceRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('parking/', ParkingSpaceListCreateAPIView.as_view(), name='parking-list-create'),
    path('parking/<int:pk>/', ParkingSpaceRetrieveUpdateDestroyAPIView.as_view(), name='parking-detail'),
]
