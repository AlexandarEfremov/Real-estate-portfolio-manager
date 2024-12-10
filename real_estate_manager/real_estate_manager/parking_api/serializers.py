from rest_framework import serializers

from real_estate_manager.parking_api.models import ParkingSpace
from real_estate_manager.tenants.models import Tenant


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = '__all__'  # Include all fields in the Parking model
        read_only_fields = ('owner',)  # Make 'owner' read-only

        extra_kwargs = {
            'size': {'help_text': 'Size in square meters (e.g., 25.5)'},
            'monthly_rent': {'help_text': 'Monthly rent in USD (e.g., 150.00)'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter the tenant queryset to only include tenants of the logged-in user
        user = self.context['request'].user  # Get the logged-in user

        # Update the queryset for the 'tenant' field to only include tenants related to the logged-in user
        self.fields['tenant'].queryset = Tenant.objects.filter(owner=user)

    def validate_monthly_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("Monthly rate must be a positive value.")
        return value

    def create(self, validated_data):
        # Automatically assign the current user to the 'owner' field when creating a ParkingSpace
        user = self.context['request'].user  # Get the logged-in user
        validated_data['owner'] = user

        # Call the parent class's create method to create the object
        return super().create(validated_data)