from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from real_estate_manager.parking_api.models import ParkingSpace
from real_estate_manager.parking_api.serializers import ParkingSerializer

class ParkingSpaceListCreateAPIView(generics.ListCreateAPIView):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can interact

    def perform_create(self, serializer):
        # Optionally set the owner to the logged-in user
        # You could also associate parking spaces with a tenant or property as needed
        serializer.save(owner=self.request.user)


class ParkingSpaceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParkingSpace.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can interact

    def get_object(self):
        # Override to ensure the logged-in user can only access their own parking spaces
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to access this parking space.")
        return obj


