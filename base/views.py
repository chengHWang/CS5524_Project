from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def base(request):
    return HttpResponse('Home page of base, the input url is /base/')

def map(request):
    return render(request, 'base/map.html')

def test(request):
    cood = list(request.GET.keys())[0].split(',')
    cood_x = int(cood[0])
    cood_y = int(cood[1])
    print(cood_x,cood_y)
    return HttpResponse('See details in terminal')