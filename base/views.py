from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import api_loader

def parse_time(time_stamp):
    hour, min, _, _ = time_stamp.split('T')[1].split(':')
    return hour, min


def weather(request):
    try:
        cood = list(request.GET.keys())[0].split(',')
        cood_x = int(cood[0])
        cood_y = int(cood[1])
        # print(cood_x,cood_y)
    except:
        cood_x = 360
        cood_y = 230

    top_la = 1.493
    bot_la = 1.1616
    left_lo = 103.590
    right_lo = 104.115

    la = top_la - (top_la-bot_la)*(cood_y/460)
    lo = left_lo + (right_lo-left_lo)*(cood_x/720)
    print(f'{cood_x,cood_y} --> {round(lo,4), round(la,4)}')


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
    # pollutant
    pollutant = api_loader._get_pollutant_standard(la, lo)
    # forecase
    forecast, forecast_update_timestamp, valid_start, valid_end = api_loader._get_weather_forecast_by_coordinate(la,lo)
    forecast_update_timestamp_hour, forecast_update_timestamp_min = parse_time(forecast_update_timestamp)
    valid_start_hour, valid_start_min = parse_time(valid_start)
    valid_end_hour, valid_end_min = parse_time(valid_end)




    context = {'temperature': temperature,
                'temperature_update_hour': temperature_update_hour,
                'temperature_update_min': temperature_update_min,

                'uv': uv,
                'uv_update_hour': uv_update_hour,
                'uv_update_min': uv_update_min,

                'pm25': pm25,
                'pm25_update_hour': pm25_update_hour,
                'pm25_update_min': pm25_update_min,

                'pollutant': pollutant,

                'forecast': forecast,
                'forecast_update_timestamp_hour': forecast_update_timestamp_hour,
                'forecast_update_timestamp_min':forecast_update_timestamp_min,
                'valid_start_hour': valid_start_hour,
                'valid_start_min':valid_start_min,
                'valid_end_hour': valid_end_hour,
                'valid_end_min':valid_end_min,
               }
    return render(request, 'base/weather.html', context)


def stores(request):
    context = {}
    return render(request, 'base/stores.html', context)


def home(request):
    # service_name = ['Select Place', 'Travel Helper', 'Spot Places']
    # service_url_name = ['map', 'weather', 'stores']
    # context = {'service_name': service_name,
    #             'service_url_name': service_url_name,}
    context = {}
    return render(request, 'base/home.html', context)

def message(request):
    messages.info(request, 'Your password has been changed successfully!')
    return HttpResponse('Message')