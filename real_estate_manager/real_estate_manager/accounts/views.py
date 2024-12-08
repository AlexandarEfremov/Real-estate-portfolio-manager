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
    success_url = reverse_lazy("login")

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

        # Calculate total income associated with the user
        context['total_income'] = sum([income.amount for income in Income.objects.filter(user=self.request.user)])

        # Calculate total expenses associated with the user
        context['total_expenses'] = sum([expense.amount for expense in Expense.objects.filter(user=self.request.user)])

        return context

class AboutPageView(TemplateView):
    template_name = "common/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #TODO Add any additional context if needed
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
        # Add any logic to handle the form data if necessary (e.g., logging)
        # For demo purposes, no actual email will be sent.
        self.request.session['contact_success'] = True  # Add a flag for confirmation
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check for success flag
        context['contact_success'] = self.request.session.pop('contact_success', False)
        return context

def faq(request):
    return render(request, 'public/faq.html')