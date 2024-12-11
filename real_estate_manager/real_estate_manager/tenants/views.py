from decimal import Decimal
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Tenant
from .forms import TenantForm
from real_estate_manager.finance.models import Income
from django.contrib import messages


class ListTenantsView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'tenants/tenant_list.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        return Tenant.objects.filter(owner=self.request.user)


class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    template_name = 'tenants/tenant_detail.html'
    context_object_name = 'tenant'

    def get_queryset(self):
        return Tenant.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = context['tenant']

        # Lease dates
        lease_start = tenant.lease_start_date
        lease_end = tenant.lease_end_date

        lease_duration = lease_end - lease_start
        total_days = lease_duration.days

        income_records = tenant.income_records.all()

        total_actual_income = income_records.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')

        daily_rent = Decimal(tenant.monthly_rent) / Decimal(30)

        projected_income = (daily_rent * Decimal(total_days)).quantize(Decimal('0.01'))

        today = timezone.now().date()
        days_passed = (today - lease_start).days
        remaining_days = max(0, total_days - days_passed)

        progress_percentage = (days_passed / total_days) * 100 if total_days > 0 else 0

        context.update({
            'projected_income': projected_income,
            'remaining_days': remaining_days,
            'progress_percentage': progress_percentage,
            'total_actual_income': total_actual_income.quantize(Decimal('0.01')),
            'income_records': income_records,  # Pass income records for additional detail
        })

        return context


class CreateTenantView(LoginRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm  # Use the custom TenantForm
    template_name = 'tenants/tenant_form.html'

    def form_valid(self, form):
        """
        Override form_valid to automatically assign the logged-in user as the owner
        of the tenant and create the projected income record.
        """
        form.instance.owner = self.request.user

        response = super().form_valid(form)

        return response

    def get_form_kwargs(self):
        """
        Override get_form_kwargs to pass the logged-in user to the form,
        which is necessary to filter the properties for the user.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        """
        After a successful form submission, redirect to the tenant list view.
        """
        return reverse_lazy('list_tenants')




class TenantEditView(LoginRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm  # Use the custom TenantForm
    template_name = 'tenants/tenant_form.html'

    def get_queryset(self):
        return Tenant.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        tenant = form.save(commit=False)

        if tenant.monthly_rent != self.object.monthly_rent:
            income_record = Income.objects.filter(tenant=tenant).first()

            if income_record:
                income_record.amount = tenant.monthly_rent
                income_record.projected_income = tenant.calculate_projected_income()
                income_record.save()

                messages.success(self.request, "Tenant details updated, including rent.")

            else:
                tenant.create_income_record()
                messages.success(self.request, "Tenant details updated with new rent.")

        else:
            tenant.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("finance:income_list")


class TenantDeleteView(LoginRequiredMixin, DeleteView):
    model = Tenant
    template_name = 'tenants/tenant_confirm_delete.html'
    context_object_name = 'tenant'

    def get_queryset(self):
        return Tenant.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('list_tenants')



