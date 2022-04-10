from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('weather/', views.weather, name='weather'),
    path('stores/', views.stores, name='stores'),
]

# urlpatterns += staticfiles_urlpatterns()