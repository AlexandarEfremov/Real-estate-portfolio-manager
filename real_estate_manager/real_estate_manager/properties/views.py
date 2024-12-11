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

# Property Create View (CBV)
class PropertyCreateView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Assign the logged-in user as the owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list_properties')  # Redirect to the property list after successful creation

class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user).order_by('created_at')

# Property Update View (CBV)
class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_form.html'

    def get_success_url(self):
        return reverse_lazy('list_properties')  # Redirect to the property list after successful update


# Property Delete View (CBV)
class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('list_properties')  # Redirect to the property list after successful deletion


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_object(self, queryset=None):
        # Retrieve the property by its pk, assuming it's owned by the logged-in user
        return get_object_or_404(Property, pk=self.kwargs['pk'])


class AsyncSearchView(View):
    async def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')

        # Ensure the logged-in user is used for filtering
        user = request.user

        # Perform the async search for both properties and tenants concurrently, filtered by the logged-in user
        properties, tenants = await asyncio.gather(
            self.search_properties(user, query),
            self.search_tenants(user, query)
        )

        # Fetch tenant properties using sync_to_async
        tenant_property_info = await asyncio.gather(
            *[self.get_tenant_property(tenant) for tenant in tenants]
        )

        # Attach tenant property info to tenants
        for idx, tenant in enumerate(tenants):
            tenant.property_info = tenant_property_info[idx]

        return render(request, 'private/search_results_partial.html', {
            'properties': properties,
            'tenants': tenants,
            'query': query,
        })

    @sync_to_async
    def search_properties(self, user, query):
        # Perform the property search asynchronously for the logged-in user
        return list(Property.objects.filter(owner=user).filter(name__icontains=query))

    @sync_to_async
    def search_tenants(self, user, query):
        # Perform the tenant search asynchronously for the logged-in user
        return list(Tenant.objects.filter(owner=user).filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ))

    @sync_to_async
    def get_tenant_property(self, tenant):
        # Fetch the related property of the tenant asynchronously
        return tenant.property.name if tenant.property else None
