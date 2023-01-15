from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Zone, Topic
from .forms import ZoneForm

def loginPage(request):   
    page ='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration. Please observe the registration rules.')


    context ={'form': form}
    return render(request, 'base/login_register.html', context)


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

    zone_count = zones.count()
    
    context = {'zones':zones, 'topics':topics, 'zone_count' : zone_count }
    
    return render(request, 'base/home.html', context)

def zone(request, pk):
    zone = Zone.objects.get(id=pk) # retrieve zone from db
    gossips = zone.gossip_set.all().order_by('-created')

    context = {'zone': zone, 'gossips': gossips}

    return render(request, 'base/zone.html', context)

# restricted to logged in users
@login_required(login_url='login')
def createZone(request):
    form = ZoneForm()

    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #return back to homepage

    context = {'form': form}
    return render(request, 'base/zone_form.html', context)

# restricted to logged in users
@login_required(login_url='login')
def updateZone(request, pk):
    zone = Zone.objects.get(id=pk)
    form = ZoneForm(instance=zone)

    if request.user != zone.host:
        return HttpResponse('You must be the creator of the zone to edit it')


    if request.method == 'POST':
        form = ZoneForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('home') #return back to homepage

    context = {'form': form}
    return render(request, 'base/zone_form.html', context)

# restricted to logged in users
@login_required(login_url='login')
def deleteZone(request, pk):
    zone = Zone.objects.get(id=pk)

    if request.user != zone.host:
        return HttpResponse('You must be the creator of the zone to delete it')

    if request.method == 'POST':
        zone.delete()
        return redirect('home') #return back to homepage

    return render(request, 'base/delete_zone.html', {'obj': zone })
