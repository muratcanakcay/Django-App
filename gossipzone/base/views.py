from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Zone, Topic, Gossip
from .forms import ZoneForm, UserForm

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
    topics = Topic.objects.all()[0:4]
    gossips = Gossip.objects.filter(Q(zone__topic__name__icontains=q))

    zone_count = zones.count()
    
    context = {'zones':zones, 'topics':topics, 'zone_count' : zone_count, 'gossips': gossips }
    
    return render(request, 'base/home.html', context)

def zone(request, pk):
    zone = Zone.objects.get(id=pk) # retrieve zone from db
    gossips = zone.gossip_set.all()
    participants = zone.participants.all().order_by('username')

    if request.method == 'POST':
        gossip = Gossip.objects.create(
            user=request.user,
            zone=zone,
            body=request.POST.get('body')
        )
        zone.participants.add(request.user)
        return redirect('zone', pk=zone.id)

    context = {'zone': zone, 'gossips': gossips, 'participants': participants}

    return render(request, 'base/zone.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    zones = user.zone_set.all()
    gossips = user.gossip_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'zones': zones, 'gossips': gossips, 'topics': topics}
    return render(request, 'base/profile.html', context)


# restricted to logged in users
@login_required(login_url='login')
def createZone(request):
    form = ZoneForm()
    topics = Topic.objects.all()
    page = 'create'

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Zone.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )       
        return redirect('home') #return back to homepage

    context = {'form': form, 'topics': topics, 'page':page}
    return render(request, 'base/zone_form.html', context)

# restricted to logged in users
@login_required(login_url='login')
def updateZone(request, pk):
    zone = Zone.objects.get(id=pk)
    form = ZoneForm(instance=zone)
    topics = Topic.objects.all()

    if request.user != zone.host:
        return HttpResponse('You must be the creator of the zone to edit it')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        zone.name = request.POST.get('name')
        zone.topic = topic
        zone.description = request.POST.get('description')     
        zone.save()   
       
        return redirect('home') #return back to homepage

    context = {'form': form, 'topics': topics, 'zone': zone}
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

    return render(request, 'base/delete.html', {'obj': zone })

# restricted to logged in users
@login_required(login_url='login')
def deleteGossip(request, pk):
    gossip = Gossip.objects.get(id=pk)

    if request.user != gossip.user:
        return HttpResponse('You must be the creator of the gossip to delete it')

    if request.method == 'POST':
        gossip.delete()
        return redirect('home') #return to homepage

    return render(request, 'base/delete.html', {'obj': gossip })

# restricted to logged in users
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)


    context ={'form': form}
    return render(request, 'base/update_user.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    zone_count = Zone.objects.all().count()
    
    context = {'topics' : topics, 'zone_count': zone_count}
    return render(request, 'base/topics.html', context)
