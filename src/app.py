import config
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup



bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def welcome(message):
    btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_btn = types.KeyboardButton("Давай!")
    no_btn = types.KeyboardButton("Не надо!")
    btns.add(yes_btn, no_btn)
    welcome_sticker = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, welcome_sticker)
    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}!\nХочешь узнать случайный факт?".format(message.from_user),
        parse_mode='html', reply_markup=btns
    )


@bot.message_handler(content_types=['text'])
def send_fact(message):
    if message.chat.type == 'private':
        if message.text == 'Давай!':
            parse_url = config.PARSE_URL
            response = requests.get(parse_url)
            page = BeautifulSoup(response.text, features="html.parser")
            fact = page.find('td')
            fact_sticker = open('static/fact.webp', 'rb')
            bot.send_sticker(message.chat.id, fact_sticker)
            bot.send_message(message.chat.id, fact.text)
            print(fact.text)
        elif message.text == 'Не надо!':
            bye_sticker = open('static/bye.webp', 'rb')
            bot.send_sticker(message.chat.id, bye_sticker)
            bot.send_message(message.chat.id, "Окей, захочешь узнать что-то интересное - заходи!")
        else:
            unknown_sticker = open('static/unknown.webp', 'rb')
            bot.send_sticker(message.chat.id, unknown_sticker)
            bot.send_message(message.chat.id, "Я хз что тебе ответить!")

bot.polling()
