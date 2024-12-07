from django import forms
from .models import Tenant
from real_estate_manager.properties.models import Property

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [
            'first_name',
            'last_name',
            'contact_info',
            'property',
            'lease_start_date',
            'lease_end_date',
            'monthly_rent',
            'image'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter contact information (email, phone)'}),
            'property': forms.Select(attrs={'class': 'form-control'}),
            'lease_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lease_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter monthly rent'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Capture the 'user' argument passed to the form
        user = kwargs.pop('user')  # Capture the 'user' argument if it's passed
        super().__init__(*args, **kwargs)

        if user:
            # Filter the properties to show only the ones owned by the user
            self.fields['property'].queryset = user.properties.all()
