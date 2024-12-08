from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Property
from .forms import PropertyForm

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

