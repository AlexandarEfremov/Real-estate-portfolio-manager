from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from real_estate_manager.accounts.views import UserRegistrationView, LandingPageView, PrivateLandingPageView, \
    AboutPageView, ContactPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('private-landing/', PrivateLandingPageView.as_view(), name='private_landing'),
    path("about/", AboutPageView.as_view(), name="about"),
    path("contact/", ContactPageView.as_view(), name="contact"),
]