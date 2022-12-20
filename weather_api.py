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
        link = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        temp = data['main']['temp']
        feel_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        wind_direction = get_wind_direction(wind_deg)
        weather = [f'В городе {city_name} сейчас {weather_desc}!\nТемпература: <b>{temp} °C</b>, чувствуется как <b>{feel_like} °C</b>.\nВетер <b>{wind_direction}</b>, <b>{wind_speed}</b> метров в секунду.', link] #<img src="https://openweathermap.org/img/wn/{icon}@2x.png"></img>

        return weather
    except Exception as ex:
        print('Произошла ошибка: ' + str(ex))
        weather = None
        return weather

