from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('zone/<str:pk>/', views.zone, name="zone"),
]
