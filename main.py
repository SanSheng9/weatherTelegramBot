import telebot
from weather_api import get_weather_api
from telebot import types
import time

bot = telebot.TeleBot('5891154215:AAEc37wi9CZjsq5NGnC73MHVC7M9vugvdjs')


# The starting message of the bot || Стартовое сообщение бота
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

#  Display information about the weather || Выводим информацию о погоде
@bot.message_handler()
def get_weather(message):
    if message.content_type == 'text':
        # Send a user request to get an array of data and an image || Отправляем запрос пользователя, чтобы получить массив данных и картинку
        data = get_weather_api(message.text)
        if data is not None:
            # Separating the array elements for ease of understanding || Отделяем элементы массива для простоты понимания
            weather = data[0]
            icon = data[1]
            # Creating a button in which we pass two parameters || Создаем кнопку, в которой мы передаем два параметра
            markup = types.InlineKeyboardMarkup()
            button_sub = types.InlineKeyboardButton(text='Подписаться', callback_data=f'sub {message.text}')
            markup.add(button_sub)
            # And create message || И создаем сообщение
            bot.send_photo(message.chat.id, icon)
            bot.send_message(message.chat.id, weather, parse_mode='html', reply_markup=markup)
            bot.send_message(message.chat.id, "Погоду из какого города мне показать?", parse_mode='html')
        # If get an error in the request, the function returns None || Если получаем ошибку в запросе, то функция возвращает None
        if data is None:
            bot.send_message(message.chat.id, 'Попробуй другой город', parse_mode='html')


# Subscription function is called every time at a user-defined time interval || Функция подписки, вызывается каждый раз в определенный пользователем интервал времени
def sub_weather(city, num, text):
    # Send a user request to get an array of data and an image || Отправляем запрос пользователя, чтобы получить массив данных и картинку
    data = get_weather_api(city)
    # I decided that the picture is unwanted here || Принял решение, что картинка здесь лишняя
    weather = data[0]
    # Creating a button where the user selects a time interval || Создаем кнопку, где пользователь выбирает интервал времени
    markup = types.InlineKeyboardMarkup()
    unsub_button = types.InlineKeyboardButton(text='Отписаться', callback_data='unsub unsub')
    change_time_button = types.InlineKeyboardButton(text='Частота получения погоды', callback_data='time unsub')
    markup.add(unsub_button, change_time_button)
    bot.send_message(num, weather, parse_mode='html', reply_markup=markup)

# A function that catches button clicks || Функция которая отлавливает нажатия на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # We divide the incoming string into an array of two elements, the first of which defines the function of the button, and the second the parameters that are necessary to perform this function, example req = ['sub', 'Paris']
    # || Приходящую строку делим на массив из двух элементов, первый из которых определяет функцию кнопки, а второй параметры, которые необходимы для выполнения этой функции, например req = ['sub', 'Владивосток']
    req = call.data.split()
    global town
    global sub
    seconds = 2 * 60 * 60
    # Subscription button || Кнопка подписки
    if req[0] == 'sub':
        bot.send_message(call.message.chat.id, 'Каждые два часа я буду присылать вам погоду 😳', parse_mode='html')
        town = req[1]
        sub = True
        print(req)
    # Unsubscribe button || Кнопка отписки
    if req[0] == 'unsub':
        sub = False
        bot.send_message(call.message.chat.id, "Погоду из какого города мне показать?", parse_mode='html')
        print(req)
    # Interval change button || Кнопка смены интервала
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
    # Interval time selection button || Кнопка выбора времени интервала
    if req[0] == 'change':
        seconds = int(req[1]) * 60 * 60
        sub = True
        bot.send_message(call.message.chat.id, f"Я буду показывать погоду каждый {req[1]} часа", parse_mode='html')
        print(req)
    # Timer || Таймер
    while sub:
        time.sleep(seconds)
        sub_weather(town, call.message.chat.id, call.message.text)
        print("Req:" + str(req) + '\nSeconds: ' + str(seconds))

if __name__ == '__main__':
    bot.polling(none_stop=True)
