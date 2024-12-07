from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from ..properties.models import Property


class IncomeCreateUpdateView(LoginRequiredMixin, CreateView, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('income_id'):
            return Income.objects.get(id=self.kwargs['income_id'])
        return None

    def form_valid(self, form):
        # Ensure the income is linked to the current user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finance:income_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the current user to the form so it can filter properties
        form = context.get('form')
        if form:
            # We explicitly set the queryset for properties to be only those belonging to the logged-in user
            form.fields['property'].queryset = Property.objects.filter(owner=self.request.user)

        return context

class ExpenseCreateUpdateView(LoginRequiredMixin, CreateView, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/expense_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('expense_id'):
            return Expense.objects.get(id=self.kwargs['expense_id'])
        return None

    def form_valid(self, form):
        # Ensure the expense is linked to the current user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finance:expense_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the current user to the form so it can filter properties
        form = context.get('form')
        if form:
            # We explicitly set the queryset for properties to be only those belonging to the logged-in user
            form.fields['property'].queryset = Property.objects.filter(owner=self.request.user)

        return context

class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expense/expense_details.html'
    context_object_name = 'expense'

    def get_object(self, queryset=None):
        """
        Override the get_object method to ensure that only expenses related
        to the logged-in user are returned.
        """
        expense = get_object_or_404(Expense, pk=self.kwargs['pk'], user=self.request.user)
        return expense

# List Views
class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'incomes'

    def get_queryset(self):
        # Filter income records by the logged-in user
        return Income.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total income
        total_income = Income.objects.filter(user=self.request.user).aggregate(total=Sum('amount'))['total'] or 0
        context['total_income'] = total_income

        return context

class IncomeDetailView(DetailView):
    model = Income
    template_name = 'income/income_details.html'
    context_object_name = 'income'

    def get_object(self, queryset=None):
        income = get_object_or_404(Income, pk=self.kwargs['pk'], user=self.request.user)
        return income

class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'income/income_confirm_delete.html'
    context_object_name = 'income'
    success_url = reverse_lazy('finance:income_list')  # Redirect to income list after deletion

    def get_object(self, queryset=None):
        income = get_object_or_404(Income, pk=self.kwargs['pk'], user=self.request.user)
        return income


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expense/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        # Filter expense records by the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total expenses
        total_expenses = Expense.objects.filter(user=self.request.user).aggregate(total=Sum('amount'))['total'] or 0
        context['total_expenses'] = total_expenses

        return context

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expense/expense_confirm_delete.html'
    context_object_name = 'expense'

    def get_object(self, queryset=None):
        """
        Ensure that only expenses related to the logged-in user are deleted.
        """
        expense = get_object_or_404(Expense, pk=self.kwargs['pk'], user=self.request.user)
        return expense

    def get_success_url(self):
        return reverse_lazy('finance:expense_list')
