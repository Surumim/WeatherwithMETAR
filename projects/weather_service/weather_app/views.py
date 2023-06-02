from django.shortcuts import render
from django.template import loader

# Create your views here.
import requests
from metar import Metar

def get_weather(request):
    if request.method == 'POST':
        if  '서울' == request.POST['station']:
           station = 'RKSM'
        elif  '인천' == request.POST['station']:
            station = 'RKSI'
        elif  '수원' == request.POST['station']:
            station = 'RKSW'
        elif  '청주' == request.POST['station']:
            station = 'RKTU'
        elif  '원주' == request.POST['station']:
            station = 'RKNW'
        elif  '군산' == request.POST['station']:
            station = 'RKJK'
        elif  '울산' == request.POST['station']:
            station = 'RKPU'
        elif  '제주도' == request.POST['station']:
            station = 'RKPC' 
        else :
            return render(request,'weather_app/errCon.html')
        
        # METAR 데이터 가져오기
        response = requests.get(f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{station.upper()}.TXT")
        response.content.decode('utf-8')
        txt = response.text

        lines = txt.split('\n')
        filtered_txt = '\n'.join(lines[1:])
        data = filtered_txt
        metar = Metar.Metar(data)

        context = {
            'station_name': request.POST['station'],
            'station_code': metar.station_id,
            'time': metar.time.ctime(),
            'temperature': metar.temp.string('C'),
            'wind_speed': metar.wind(),  
            'visibility': metar.visibility(),
            'pre_weather': metar.present_weather(),
        }

        return render(request,'weather_app/weather.html',context)

    return render(request,'weather_app/index.html')
