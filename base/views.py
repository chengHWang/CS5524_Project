from django.shortcuts import render
from django.http import HttpResponse
import api_loader

def parse_time(time_stamp):
    hour, min, _, _ = time_stamp.split('T')[1].split(':')
    return hour, min

# def map(request):
#     return render(request, 'base/map.html')

def weather(request):
    la, lo = 1.3135,103.9625
    # temperature
    api_reader = api_loader._get_air_temp_by_coordinate(la, lo)
    temperature = api_reader[0]
    temperature_update_hour, temperature_update_min = parse_time(api_reader[1])
    # uv
    api_reader = api_loader._get_uv()
    uv = api_reader[0]
    uv_update_hour, uv_update_min = parse_time(api_reader[1])

    # pm2.5
    api_reader = api_loader._get_pm25_by_coordinate(la, lo)
    pm25 = api_reader[0]
    pm25_update_hour, pm25_update_min = parse_time(api_reader[1])

    
    pollutant = api_loader._get_pollutant_standard(la, lo)

    context = {'temperature': temperature,
                'temperature_update_hour': temperature_update_hour,
                'temperature_update_min': temperature_update_min,
                'uv': uv,
                'uv_update_hour': uv_update_hour,
                'uv_update_min': uv_update_min,
                'pm25': pm25,
                'pm25_update_hour': pm25_update_hour,
                'pm25_update_min': pm25_update_min,
                
                
                'pollutant': pollutant}
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
    # service_name = ['Select Place', 'Travel Helper', 'Spot Places']
    # service_url_name = ['map', 'weather', 'stores']
    # context = {'service_name': service_name,
    #             'service_url_name': service_url_name,}
    context = {}
    return render(request, 'base/home.html', context)

