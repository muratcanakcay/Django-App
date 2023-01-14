from django.shortcuts import render, redirect
from .models import Zone
from .forms import ZoneForm

def home(request):
    zones = Zone.objects.all() # retrieve zones from db
    context = {'zones':zones}
    return render(request, 'base/home.html', context)

def zone(request, pk):
    zone = Zone.objects.get(id=pk) # retrieve zone from db
    context = {'zone': zone}

    return render(request, 'base/zone.html', context)

def createZone(request):
    form = ZoneForm()

    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #return back to homepage

    context = {'form': form}
    return render(request, 'base/zone_form.html', context)

def updateZone(request, pk):
    zone = Zone.objects.get(id=pk)
    form = ZoneForm(instance=zone)

    context = {'form': form}
    return render(request, 'base/zone_form.html', context)