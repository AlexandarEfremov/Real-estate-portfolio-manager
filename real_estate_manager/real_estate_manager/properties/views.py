from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .forms import PropertyForm
from django.views import View
from asgiref.sync import sync_to_async
from real_estate_manager.properties.models import Property
from real_estate_manager.tenants.models import Tenant
import asyncio

class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list_properties')

class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user).order_by('created_at')

class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'

    def get_success_url(self):
        return reverse_lazy('list_properties')

class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('list_properties')


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_object(self, queryset=None):
        return get_object_or_404(Property, pk=self.kwargs['pk'])


class AsyncSearchView(View):
    async def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')

        user = request.user

        properties, tenants = await asyncio.gather(
            self.search_properties(user, query),
            self.search_tenants(user, query)
        )

        tenant_property_info = await asyncio.gather(
            *[self.get_tenant_property(tenant) for tenant in tenants]
        )

        for idx, tenant in enumerate(tenants):
            tenant.property_info = tenant_property_info[idx]

        return render(request, 'private/search_results_partial.html', {
            'properties': properties,
            'tenants': tenants,
            'query': query,
        })

    @sync_to_async
    def search_properties(self, user, query):
        return list(Property.objects.filter(owner=user).filter(name__icontains=query))

    @sync_to_async
    def search_tenants(self, user, query):
        return list(Tenant.objects.filter(owner=user).filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ))

    @sync_to_async
    def get_tenant_property(self, tenant):
        return tenant.property.name if tenant.property else None
