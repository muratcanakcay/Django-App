from django.shortcuts import render

zones = [
    {'id':1, 'name':'Nude photos of Britney Spears!'},
    {'id':2, 'name':'Tina from the bookstore'},
    {'id':3, 'name':'Chad has a child?'},
]

def home(request):
    context = {'zones':zones}
    return render(request, 'home.html', context)

def zone(request):
    return render(request, 'zone.html')