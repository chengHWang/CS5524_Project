from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
import api_loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

nus_la = 1.297
nus_lo = 103.776

def parse_time(time_stamp):
    hour, min, _, _ = time_stamp.split('T')[1].split(':')
    return hour, min

def weather(request, la, lo):
    la = float(la)
    lo = float(lo)
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

    # forecase
    forecast, forecast_update_timestamp, valid_start, valid_end = api_loader._get_weather_forecast_by_coordinate(la,lo)
    forecast_update_timestamp_hour, forecast_update_timestamp_min = parse_time(forecast_update_timestamp)
    valid_start_hour, valid_start_min = parse_time(valid_start)
    valid_end_hour, valid_end_min = parse_time(valid_end)

    # pollutant
    api_reader = api_loader._get_pollutant_standard(la, lo)
    pollutant = api_reader[0]
    pm10 = pollutant["pm10_sub_index"]
    so2 = pollutant['so2_sub_index']
    no2 = pollutant['no2_one_hour_max']
    co = pollutant['co_sub_index']
    o3 = pollutant['o3_sub_index']

    pollutant_update_hour, pollutant_update_min = parse_time(api_reader[1])

    context = {
                'curr_la':round(la, 3), 
                'curr_lo':round(lo, 3),
                'temperature': temperature,
                'temperature_update_hour': temperature_update_hour,
                'temperature_update_min': temperature_update_min,

                'uv': uv,
                'uv_update_hour': uv_update_hour,
                'uv_update_min': uv_update_min,

                'pm25': pm25,
                'pm25_update_hour': pm25_update_hour,
                'pm25_update_min': pm25_update_min,

                'pollutant_update_hour': pollutant_update_hour,
                'pollutant_update_min': pollutant_update_min, 
                'pm10': pm10,
                'so2': so2,
                'no2' : no2,
                'co' : co,
                'o3' : o3,


                'forecast': forecast,
                'forecast_update_timestamp_hour': forecast_update_timestamp_hour,
                'forecast_update_timestamp_min':forecast_update_timestamp_min,
                'valid_start_hour': valid_start_hour,
                'valid_start_min':valid_start_min,
                'valid_end_hour': valid_end_hour,
                'valid_end_min':valid_end_min,
               }
    return render(request, 'base/weather.html', context)


def stores(request, la, lo):
    la = float(la)
    lo = float(lo)
    business = api_loader._get_nearby_business(la,lo)
    if len(business) > 10:
        business = business[:10]
    number_business = len(business)

    business_sorted = sorted(business, key=lambda x: x[5], reverse=True)

    context = { 'curr_la':round(la, 3), 
                'curr_lo':round(lo, 3),
                'number_business': number_business,
                'business': business_sorted}
    return render(request, 'base/stores.html', context)


def home(request):
    business = api_loader._get_nearby_business(nus_la, nus_lo)

    context = {'curr_la': nus_la, 'curr_lo': nus_lo, 'number_business': min(len(business), 10)}
    return render(request, 'base/home.html', context)

def map(request):
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

    business = api_loader._get_nearby_business(la, lo)

    context = {'curr_la':round(la, 3), 'curr_lo':round(lo, 3), 'number_business': min(len(business), 10)}
    # context = {"pk": pk}
    # return render(request, 'base/home.html', context)
    return render(request, 'base/map.html', context)

def message(request):
    messages.info(request, 'Your password has been changed successfully!')
    return HttpResponse('Message')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
        

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)