from django import forms
from .models import Tenant

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
        """
        Custom initialization to filter the properties available to the current user.
        """
        # Get the user argument from kwargs
        user = kwargs.pop('user')  # Default to None if 'user' is not passed

        super().__init__(*args, **kwargs)

        # If the user is provided, filter the properties queryset
        if user:
            self.fields['property'].queryset = user.properties.all()
