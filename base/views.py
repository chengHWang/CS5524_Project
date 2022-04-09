from django.shortcuts import render
from django.http import HttpResponse

def map(request):
    return render(request, 'base/map.html')

def weather(request):
    context = {}
    return render(request, 'base/weather.html', context)

def stores(request):
    context = {}
    return render(request, 'base/stores.html', context)

def test(request):
    cood = list(request.GET.keys())[0].split(',')
    cood_x = int(cood[0])
    cood_y = int(cood[1])
    print(cood_x,cood_y)
    return HttpResponse('See details in terminal')

def home(request):
    service_name = ['Select Place', 'Travel Helper', 'Spot Places']
    service_url_name = ['map', 'weather', 'stores']
    context = {'service_name': service_name,
                'service_url_name': service_url_name,}
    return render(request, 'base/home.html', context)

