import telebot
from telebot import types
import requests

bot = telebot.TeleBot('5891154215:AAEc37wi9CZjsq5NGnC73MHVC7M9vugvdjs')

@bot.message_handler(commands=['start'])
def start(message):
    #button start
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button = types.KeyboardButton('Нажми на кнопку, чтобы запустить бота!')
    # markup.add(button)
    smile_message = "⛅️"
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name is not None else ''
    start_message = f'Привет, <b>{first_name} {last_name}</b>. \nБот <b>Smokie</b> будет показывать погоду на каждый день!'
    q_message = "Погоду из какого города мне показать?"
    bot.send_message(message.chat.id, smile_message, parse_mode='html')
    bot.send_message(message.chat.id, start_message, parse_mode='html')
    bot.send_message(message.chat.id, q_message, parse_mode='html')

bot.polling(none_stop=True)