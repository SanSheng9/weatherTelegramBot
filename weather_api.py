import requests


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
        weather = [
            f'В городе {city_name} сейчас {weather_desc}!\nТемпература: <b>{temp} °C</b>, чувствуется как <b>{feel_like} °C</b>.\nВетер <b>{wind_direction}</b>, <b>{wind_speed}</b> метров в секунду.',
            link]

        return weather
    except Exception as ex:
        print('Произошла ошибка: ' + str(ex))
        weather = None
        return weather


def get_wind_direction(deg):
    if deg >= 326.25 or deg <= 33.75:
        return 'северный'
    elif deg >= 33.76 and deg <= 56.25:
        return 'северо-восточный'
    elif deg >= 56.26 and deg <= 123.75:
        return 'восточный'
    elif deg >= 123.75 and deg <= 168.75:
        return 'юго-восточный'
    elif deg >= 168.76 and deg <= 213.75:
        return 'южный'
    elif deg >= 213.76 and deg <= 258.75:
        return 'западно-восточный'
    elif deg >= 258.76 and deg <= 303.75:
        return 'западный'
    elif deg >= 303.76 and deg <= 326.24:
        return 'северо-западный'
