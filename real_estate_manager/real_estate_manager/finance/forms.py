from django import forms
from .models import Income
from .models import Expense
from real_estate_manager.properties.models import Property

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'property', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in $'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'property': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description (optional)', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Filter properties to only those owned by the user
            self.fields['property'].queryset = Property.objects.filter(owner=user)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'property', 'category', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in $'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'property': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description (optional)', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Filter properties to only those owned by the user
            self.fields['property'].queryset = Property.objects.filter(owner=user)
