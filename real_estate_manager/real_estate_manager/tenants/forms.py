from django import forms
from django.core.exceptions import ValidationError

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

        error_messages = {
            'lease_start_date': {
                'required': 'Lease start date is required.',
            },
            'lease_end_date': {
                'required': 'Lease end date is required.',
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Custom initialization to filter the properties available to the current user.
        """
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        if user:
            self.fields['property'].queryset = user.properties.all()

    def clean(self):
        """
        Custom clean method to validate the relationship between lease_start_date and lease_end_date.
        """
        cleaned_data = super().clean()
        lease_start_date = cleaned_data.get('lease_start_date')
        lease_end_date = cleaned_data.get('lease_end_date')

        if lease_start_date and lease_end_date:
            if lease_end_date <= lease_start_date:
                raise ValidationError('Lease end date must be after the lease start date.')

            lease_duration = (lease_end_date - lease_start_date).days
            if lease_duration < 30:
                raise ValidationError('The lease duration must be at least 30 days.')

        return cleaned_data