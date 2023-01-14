from django.shortcuts import render
from .models import Zone

# zones = [
#     {'id':1, 'name':'Nude photos of Britney Spears!'},
#     {'id':2, 'name':'Tina from the bookstore'},
#     {'id':3, 'name':'Chad has a child?'},
# ]

def home(request):
    zones = Zone.objects.all() # retrieve zones from db
    context = {'zones':zones}
    return render(request, 'base/home.html', context)

def zone(request, pk):
    zone = Zone.objects.get(id=pk) # retrieve zone from db
    context = {'zone': zone}

    return render(request, 'base/zone.html', context)