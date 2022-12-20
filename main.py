import telebot
from weather_api import get_weather_api
from telebot import types
import time

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


@bot.message_handler()
def get_weather(message):
    if message.content_type == 'text':
        data = get_weather_api(message.text)
        if data is not None:
            weather = data[0]
            icon = data[1]
            markup = types.InlineKeyboardMarkup()
            button_sub = types.InlineKeyboardButton(text='Подписаться', callback_data=f'sub {message.text}')
            markup.add(button_sub)
            bot.send_photo(message.chat.id, icon)
            bot.send_message(message.chat.id, weather, parse_mode='html', reply_markup=markup)
            bot.send_message(message.chat.id, "Погоду из какого города мне показать?", parse_mode='html')
        if data is None:
            bot.send_message(message.chat.id, 'Попробуй другой город', parse_mode='html')
        # print('Data: ' + str(data) + '\nMessage: ' + str(message.text))


def sub_weather(city, num, text):
    data = get_weather_api(city)
    weather = data[0]
    markup = types.InlineKeyboardMarkup()
    unsub_button = types.InlineKeyboardButton(text='Отписаться', callback_data='unsub unsub')
    change_time_button = types.InlineKeyboardButton(text='Частота получения погоды', callback_data='time unsub')
    markup.add(unsub_button, change_time_button)
    bot.send_message(num, weather, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global sub
    req = call.data.split()
    seconds = 2 * 60 * 60
    global town
    # args = [req[1], call.message.chat.id, call.message.text]
    # timer = threading.Timer(time, sub_weather, args=args)
    if req[0] == 'sub':
        bot.send_message(call.message.chat.id, 'Каждые два часа я буду присылать вам погоду 😳', parse_mode='html')
        town = req[1]
        sub = True
        print(req)
    if req[0] == 'unsub':
        sub = False
        bot.send_message(call.message.chat.id, "Погоду из какого города мне показать?", parse_mode='html')
        print(req)
    if req[0] == 'time':
        sub = False
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text='2 часа', callback_data='change 2')
        item2 = types.InlineKeyboardButton(text='4 часа', callback_data='change 4')
        item3 = types.InlineKeyboardButton(text='6 часа', callback_data='change 6')
        item4 = types.InlineKeyboardButton(text='24 часа', callback_data='change 24')
        markup.add(item1, item2, item3, item4)
        bot.send_message(call.message.chat.id, "Через сколько мне показывать погоду?", parse_mode='html', reply_markup=markup)
        print(req)
    if req[0] == 'change':
        seconds = int(req[1]) * 60 * 60
        sub = True
        bot.send_message(call.message.chat.id, f"Я буду показывать погоду каждый {req[1]} часа", parse_mode='html')
        print(req)
    while sub:
        time.sleep(seconds)
        sub_weather(town, call.message.chat.id, call.message.text)
        print("Req:" + str(req) + '\nSeconds: ' + str(seconds))

if __name__ == '__main__':
    bot.polling(none_stop=True)
