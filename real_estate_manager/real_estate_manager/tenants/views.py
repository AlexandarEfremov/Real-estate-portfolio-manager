from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tenant
from .forms import TenantForm

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
        # Ensure that the tenant belongs to the logged-in user
        return Tenant.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add property information to context to access it in the template
        tenant = context['tenant']
        context['property'] = tenant.property
        return context

class CreateTenantView(LoginRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm  # Use the custom TenantForm
    template_name = 'tenants/tenant_form.html'

    def form_valid(self, form):
        # Automatically assign the logged-in user as the owner of the tenant
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

    def get_success_url(self):
        # Redirect to the tenant list view after successful creation
        return reverse_lazy('list_tenants')

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

    def get_success_url(self):
        # Redirect to the tenant detail view after successful update
        return reverse_lazy('tenant_detail', kwargs={'pk': self.object.pk})

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
