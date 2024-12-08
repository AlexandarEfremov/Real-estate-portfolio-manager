from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.mixins import LoginRequiredMixin

from ..properties.models import Property
from ..tenants.models import Tenant


class IncomeCreateUpdateView(LoginRequiredMixin, CreateView, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('income_id'):
            return Income.objects.get(id=self.kwargs['income_id'], user=self.request.user)
        return None

    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure income is linked to logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finance:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' in context:
            context['form'].fields['tenant'].queryset = Tenant.objects.filter(owner=self.request.user)
        return context


class ExpenseCreateUpdateView(LoginRequiredMixin, CreateView, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/expense_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('expense_id'):
            return Expense.objects.get(id=self.kwargs['expense_id'], user=self.request.user)
        return None

    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure expense is linked to logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finance:expense_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' in context:
            # Pass the current user to the form so that it filters the tenants and properties accordingly
            context['form'].fields['tenant'].queryset = Tenant.objects.filter(owner=self.request.user)
            context['form'].fields['property'].queryset = Property.objects.filter(owner=self.request.user)
        return context


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expense/expense_details.html'
    context_object_name = 'expense'

    def get_object(self, queryset=None):
        """Ensure only expenses related to the logged-in user are returned."""
        return get_object_or_404(Expense, pk=self.kwargs['pk'], user=self.request.user)

class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'tenant_incomes'

    def get_queryset(self):
        # Fetch all income records for the logged-in user
        return Income.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch tenants whose properties belong to the current user
        tenants = Tenant.objects.filter(property__owner=self.request.user)

        total_projected_income = Decimal(0)

        # Loop through tenants and calculate their projected income
        for tenant in tenants:
            lease_start = tenant.lease_start_date
            lease_end = tenant.lease_end_date

            # Calculate total days in the lease
            lease_duration = lease_end - lease_start
            total_days = lease_duration.days

            # Calculate daily rent (divide by 30 for simplicity)
            daily_rent = Decimal(tenant.monthly_rent) / Decimal(30)

            # Add the projected income for this tenant
            projected_income = daily_rent * Decimal(total_days)
            total_projected_income += projected_income

        # Add to the context the total projected income for the user
        context['total_income'] = total_projected_income

        return context


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'income/income_confirm_delete.html'
    context_object_name = 'income'
    success_url = reverse_lazy('finance:income_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Income, pk=self.kwargs['pk'], user=self.request.user)


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expense/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        # Filter expense records for the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total expenses
        total_expenses = context['expenses'].aggregate(total=Sum('amount'))['total'] or 0
        context['total_expenses'] = total_expenses

        return context


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expense/expense_confirm_delete.html'
    context_object_name = 'expense'

    def get_object(self, queryset=None):
        """Ensure only expenses related to the logged-in user are deleted."""
        return get_object_or_404(Expense, pk=self.kwargs['pk'], user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('finance:expense_list')
