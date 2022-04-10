from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('map/', views.map, name="map"),
    path('weather/<str:la>/<str:lo>', views.weather, name='weather'),
    path('stores/<str:la>/<str:lo>', views.stores, name='stores'),
]

# urlpatterns += staticfiles_urlpatterns()