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

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
]

# urlpatterns += staticfiles_urlpatterns()