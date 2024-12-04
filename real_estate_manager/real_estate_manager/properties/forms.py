from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter property name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address', 'rows': 3}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter size in square meters'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter value'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
