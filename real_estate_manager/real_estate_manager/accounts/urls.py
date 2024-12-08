from django.contrib.auth.views import LogoutView
from django.urls import path

from real_estate_manager.accounts import views
from real_estate_manager.accounts.views import UserRegistrationView, LandingPageView, PrivateLandingPageView, \
    AboutPageView, ContactPageView, CustomLoginView, faq

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('private-landing/', PrivateLandingPageView.as_view(), name='private_landing'),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
    path('faq/', faq, name='faq'),
]
