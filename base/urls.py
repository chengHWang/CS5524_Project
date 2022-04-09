from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('',views.base),
    path('map/',views.map),
    path('map/#?',views.test)
]

# urlpatterns += staticfiles_urlpatterns()