from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import AccessMixin
from real_estate_manager.finance.models import Income, Expense
from real_estate_manager.forms import CustomUserCreationForm, ContactForm
from real_estate_manager.properties.models import Property
from real_estate_manager.tenants.models import Tenant

class CustomLoginView(LoginView):
    """Custom LoginView to handle login form errors."""
    template_name = "registration/login.html"

    def form_invalid(self, form):
        """Override to add custom error messages."""
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

class UserRegistrationView(CreateView):
    """Handles user registration with a custom form."""
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        """Handle successful registration."""
        user = form.save()  # Save the new user
        messages.success(self.request, f"Registration successful! Welcome, {user.username}. You can now log in.")
        return self.render_to_response(self.get_context_data(success=True, username=user.username))

    def form_invalid(self, form):
        """Override to add error messages for registration."""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)

class LandingPageView(TemplateView):
    template_name = 'common/landing_page.html'


class PrivateLandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'private/private_landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the properties of the current user
        context['properties'] = Property.objects.filter(owner=self.request.user)

        # Fetch tenants whose properties belong to the current user
        context['tenants'] = Tenant.objects.filter(property__owner=self.request.user)

        total_projected_income = Decimal(0)

        # Loop through tenants and calculate their projected income
        for tenant in context['tenants']:
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

        context['total_projected_income'] = total_projected_income

        context['total_expenses'] = sum([expense.amount for expense in Expense.objects.filter(user=self.request.user)])

        return context

class AboutPageView(TemplateView):
    template_name = "common/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class VisitorOnlyMixin(AccessMixin, View):
    """Mixin to restrict access to unauthenticated users only."""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("private_landing"))  # Redirect authenticated users
        return super().dispatch(request, *args, **kwargs)


class ContactPageView(LoginRequiredMixin, FormView):
    template_name = "public/../../templates/private/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        # For demo purposes, no actual email will be sent.
        self.request.session['contact_success'] = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_success'] = self.request.session.pop('contact_success', False)
        return context

def faq(request):
    return render(request, 'public/faq.html')