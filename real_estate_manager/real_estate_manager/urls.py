"""
URL configuration for real_estate_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from real_estate_manager import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("real_estate_manager.accounts.urls")),
    path("properties/", include("real_estate_manager.properties.urls")),
    path('tenants/', include('real_estate_manager.tenants.urls')),
    # Income URLs (for income related views)
    path('finance/', include('real_estate_manager.finance.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)