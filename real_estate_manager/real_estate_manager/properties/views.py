from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm

@login_required
def create_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('private_landing')
    else:
        form = PropertyForm()

    return render(request, 'properties/property_form.html', {'form': form})

