import config
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup



bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def welcome(message):
    btns = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_y = types.KeyboardButton("Да!")
    btn_n = types.KeyboardButton("Нет!")
    btns.add(btn_y, btn_n)
    welcome_sticker = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, welcome_sticker)
    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}!\nХочешь узнать случайный факт?".format(message.from_user),
        parse_mode='html',
        reply_markup=btns
    )


@bot.message_handler(content_types=['text'])
def send_fact(message):
    if message.chat.type == 'private':
        if message.text == 'Да!':
            parse_url = config.PARSE_URL
            response = requests.get(parse_url)
            page = BeautifulSoup(response.text, features="html.parser")
            fact = page.find('td')
            fact_sticker = open('static/fact.webp', 'rb')
            inline_btns = types.InlineKeyboardMarkup(row_width=2)
            inline_btn_g = types.InlineKeyboardButton("👍", callback_data='good')
            inline_btn_b = types.InlineKeyboardButton("👎", callback_data='bad')
            inline_btns.add(inline_btn_g, inline_btn_b)
            bot.send_sticker(message.chat.id, fact_sticker)
            bot.send_message(message.chat.id, fact.text, reply_markup=inline_btns)
            print(fact.text)
        elif message.text == 'Нет!':
            bye_sticker = open('static/bye.webp', 'rb')
            bot.send_sticker(message.chat.id, bye_sticker)
            bot.send_message(message.chat.id, "Окей, захочешь узнать что-то интересное - заходи!")
        else:
            unknown_sticker = open('static/unknown.webp', 'rb')
            bot.send_sticker(message.chat.id, unknown_sticker)
            bot.send_message(message.chat.id, "Я хз что тебе ответить!")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data)
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Показать ещё?')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Принял!\nПоказать ещё?')

            # remove inline buttons
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Спасибо за ответ!',
                reply_markup=None
            )

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
    except Exception as e:
        print(repr(e))

bot.polling()
