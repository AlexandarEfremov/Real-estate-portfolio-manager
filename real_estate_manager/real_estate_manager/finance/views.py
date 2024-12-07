from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from .models import Income, Expense
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IncomeCreateUpdateView(LoginRequiredMixin, CreateView, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('income_id'):
            return Income.objects.get(id=self.kwargs['income_id'])
        return None

    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure the income is linked to the current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finance:income_list')


class ExpenseCreateUpdateView(LoginRequiredMixin, CreateView, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense/expense_form.html'

    def get_object(self, queryset=None):
        if self.kwargs.get('expense_id'):
            return Expense.objects.get(id=self.kwargs['expense_id'])
        return None

    def form_valid(self, form):
        form.instance.user = self.request.user  # Ensure the expense is linked to the current user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('finance:expense_list')


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
