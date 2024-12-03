from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import CreateView, FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import AccessMixin

from real_estate_manager.forms import CustomUserCreationForm, ContactForm


class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class LandingPageView(TemplateView):
    template_name = 'common/landing_page.html'

class PrivateLandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'private/private_landing_page.html'

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


class ContactPageView(VisitorOnlyMixin, FormView):
    template_name = "public/contact.html"
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