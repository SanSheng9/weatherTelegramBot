import telebot
from weather_api import get_weather_api
from telebot import types

bot = telebot.TeleBot('5891154215:AAEc37wi9CZjsq5NGnC73MHVC7M9vugvdjs')


# Start weather bot
@bot.message_handler(commands=['start'])
def start(message):
    smile_message = "⛅️"
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name is not None else ''
    start_message = f'Привет, <b>{first_name} {last_name}</b>. \nБот <b>Smokie</b> будет показывать погоду на каждый день!'
    bot.send_message(message.chat.id, smile_message, parse_mode='html')
    bot.send_message(message.chat.id, start_message, parse_mode='html')
    q_message = "Погоду из какого города мне показать?"
    bot.send_message(message.chat.id, q_message, parse_mode='html')


# Get weather-json
@bot.message_handler()
def get_weather(message):
    if message.content_type == 'text':
        data = get_weather_api(message.text)
        print(data['suc'])
        if data['suc']:
            weather = f'В городе {data["city"]} сейчас {data["desc"]}!\nТемпература: <b>{data["temp"]} °C</b>, чувствуется как <b>{data["feel_like"]} °C</b>.\nВетер <b>{data["wind_direction"]}</b>, <b>{data["wind_speed"]}</b> метров в секунду.'
            bot.send_photo(message.chat.id, f'https://openweathermap.org/img/wn/{data["icon"]}@2x.png')
            bot.send_message(message.chat.id, weather, parse_mode='html')
        if not data['suc']:
            bot.send_message(message.chat.id, 'Попробуй другой город', parse_mode='html')
        # print('Data: ' + str(data) + '\nMessage: ' + str(message.text))


bot.polling(none_stop=True)
