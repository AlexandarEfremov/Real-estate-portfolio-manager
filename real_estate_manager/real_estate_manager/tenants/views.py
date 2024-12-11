from decimal import Decimal
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Tenant
from .forms import TenantForm
from real_estate_manager.finance.models import Income  # Import Income model
from django.contrib import messages


class ListTenantsView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'tenants/tenant_list.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        # Filter tenants by the logged-in user
        return Tenant.objects.filter(owner=self.request.user)


class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant
    template_name = 'tenants/tenant_detail.html'
    context_object_name = 'tenant'

    def get_queryset(self):
        # Ensure only tenants owned by the logged-in user are retrieved
        return Tenant.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = context['tenant']

        # Lease dates
        lease_start = tenant.lease_start_date
        lease_end = tenant.lease_end_date

        # Calculate total lease duration in days
        lease_duration = lease_end - lease_start
        total_days = lease_duration.days

        # Fetch actual income records for this tenant
        income_records = tenant.income_records.all()

        # Total income from actual records
        total_actual_income = income_records.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')  # Default to 0 if no records

        # Calculate daily rent using tenant's monthly rent
        daily_rent = Decimal(tenant.monthly_rent) / Decimal(30)  # Approximate daily rent for simplicity

        # Projected income based on lease period
        projected_income = (daily_rent * Decimal(total_days)).quantize(Decimal('0.01'))

        # Calculate remaining lease days
        today = timezone.now().date()
        days_passed = (today - lease_start).days
        remaining_days = max(0, total_days - days_passed)

        # Calculate lease progress percentage
        progress_percentage = (days_passed / total_days) * 100 if total_days > 0 else 0

        # Update the context with the calculated values
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
        form.instance.owner = self.request.user  # Assign the logged-in user as the owner

        # Save the tenant instance first
        response = super().form_valid(form)

        # Do not create the income record manually here
        # Tenant.save() will automatically create the income record

        return response

    def get_form_kwargs(self):
        """
        Override get_form_kwargs to pass the logged-in user to the form,
        which is necessary to filter the properties for the user.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

    def get_success_url(self):
        """
        After a successful form submission, redirect to the tenant list view.
        """
        return reverse_lazy('list_tenants')  # Ensure 'list_tenants' is the correct URL name




class TenantEditView(LoginRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm  # Use the custom TenantForm
    template_name = 'tenants/tenant_form.html'

    def get_queryset(self):
        # Ensure that the tenant belongs to the logged-in user
        return Tenant.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

    def form_valid(self, form):
        tenant = form.save(commit=False)  # Save the tenant without committing

        # Check if rent has changed
        if tenant.monthly_rent != self.object.monthly_rent:
            # If rent changed, update the existing income record
            # Find the existing income record for this tenant
            income_record = Income.objects.filter(tenant=tenant).first()

            if income_record:
                # Update the existing income record with the new rent
                income_record.amount = tenant.monthly_rent
                income_record.projected_income = tenant.calculate_projected_income()
                income_record.save()  # Save the updated income record

                messages.success(self.request, "Tenant details updated, including rent.")

            else:
                # If no income record exists, create one
                tenant.create_income_record()
                messages.success(self.request, "Tenant details updated with new rent.")

        else:
            # If rent has not changed, just save the tenant as is
            tenant.save()

        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the tenant detail view after successful update
        return reverse_lazy("finance:income_list")


class TenantDeleteView(LoginRequiredMixin, DeleteView):
    model = Tenant
    template_name = 'tenants/tenant_confirm_delete.html'
    context_object_name = 'tenant'

    def get_queryset(self):
        # Ensure that the tenant belongs to the logged-in user
        return Tenant.objects.filter(owner=self.request.user)

    def get_success_url(self):
        # Redirect to the tenant list view after successful deletion
        return reverse_lazy('list_tenants')



