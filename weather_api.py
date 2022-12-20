import requests
from wind_direction import get_wind_direction


def get_weather_api(city):
    API_key = 'bbe5d60aaa3307f217bd550c7b30441c'
    lang = 'ru'
    try:
        response = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={str(city)}&appid={API_key}&lang={lang}&units=metric')
        data = response.json()
        city_name = data["name"]
        weather_desc = data["weather"][0]["description"]
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        feel_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        wind_direction = get_wind_direction(wind_deg)
        data = {'suc': True, 'icon': icon, 'city': city_name, 'desc': weather_desc, 'temp': temp,
                'feel_like': feel_like, 'wind_speed': wind_speed, 'wind_direction': wind_direction}
        return data
    except Exception as ex:
        print('Произошла ошибка: ' + str(ex))
        data = {'suc': False}
        return data

