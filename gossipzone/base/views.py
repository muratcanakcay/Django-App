from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Zone, Topic
from .forms import ZoneForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # retrieve zones from db
    zones = Zone.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) | 
        Q(description__icontains=q) 
    ) 
    
    # retrieve topics from db
    topics = Topic.objects.all() 
    
    context = {'zones':zones, 'topics':topics }
    
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

    if request.method == 'POST':
        form = ZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('home') #return back to homepage

    context = {'form': form}
    return render(request, 'base/zone_form.html', context)

def deleteZone(request, pk):
    zone = Zone.objects.get(id=pk)

    if request.method == 'POST':
        zone.delete()
        return redirect('home') #return back to homepage

    return render(request, 'base/delete_zone.html', {'obj': zone })