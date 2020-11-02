import json
import telebot
import requests
from telebot import types

bot = telebot.TeleBot("1148909884:AAFywUYIklb21bfeGKb8gEnp8P-1Bivdf6A", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет студент, введи номер своей зачетной книжки =-)")


# Условная авторизация
@bot.message_handler(regexp="bi20i".lower())
def send_inf(message):
    global markup
    response = requests.get('http://taskbotsibadi.us.aldryn.io/bot/json_response')
    data = json.loads(response.text)
    if message.text.lower() in data:
        sum_labs = 0
        # Счетчик лабораторных, которые не сделанны
        user = message.text.lower()
        bot.send_message(message.from_user.id,
                         '%s\n%s' % (data[user]['name'], "Твой рейтинг " + str(data[user]['rating'])))
        for lab in data[user]['labs']:

            if data[user]['labs'][lab]['status'] == 0:

                sum_labs += 1
                bot.send_message(message.from_user.id,
                                 '%s\n%s\n%s' % ("Номер лабы: " + str(lab),
                                                 "Назавание лабы: " + data[user]['labs'][lab]['name'],
                                                 "Задание: " + data[user]['labs'][lab]['description']))
                # создаются кнопки, количество = количеству не выполненных лаб
                markup = types.ReplyKeyboardMarkup()
                keyboard = types.KeyboardButton(str(lab))
                markup.add(keyboard)
        if sum_labs > 0:

            bot.send_message(message.from_user.id, "Выбери номер лабораторной по которой нужны подсказки:",
                             reply_markup=markup)

        # В условии подсказки можно вызвать только при условной авторизации,
        # т.е только полсе того, как пользователь введет свой номер зачетки
        # выводятся все подсказки поочереди
        @bot.message_handler()
        def hints(message):

            for i in (data[user]['labs'][message.text]['hints']):
                bot.send_message(message.from_user.id, data[user]['labs'][str(message.text)]['hints'][str(i)])


bot.polling(none_stop=True, interval=0)
