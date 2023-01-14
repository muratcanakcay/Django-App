from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('zone/<str:pk>/', views.zone, name="zone"),
    path('create-zone/', views.createZone, name="create-zone"),
    path('update-zone/<str:pk>', views.updateZone, name="update-zone"),
    path('delete-zone/<str:pk>', views.deleteZone, name="delete-zone"),
]
