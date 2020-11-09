import json
import telebot
import requests

bot = telebot.TeleBot("1148909884:AAFywUYIklb21bfeGKb8gEnp8P-1Bivdf6A", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет студент, введи номер своей зачетной книжки =-)")


# Условная авторизация
@bot.message_handler(regexp="bi20i".lower())
def send_inf(message):
    global user

    response = requests.get('http://taskbotsibadi.us.aldryn.io/bot/json_response')
    data = json.loads(response.text)
    if message.text.lower() in data:
        sum_labs = 0

        user = user = message.text.lower()
        bot.send_message(message.from_user.id, data[user]['name'])
        for lab in data[user]['labs']:

            if data[user]['labs'][lab]['status'] == 0:
                sum_labs += 1
                bot.send_message(message.from_user.id,
                                 '%s\n%s\n%s' % ("Номер лабы: " + str(lab),
                                                 "Назавание лабы: " + data[user]['labs'][lab]['name'],
                                                 "Задание: " + data[user]['labs'][lab]['description']))

        if sum_labs > 0:
            bot.send_message(message.from_user.id, "Выбери номер лабораторной по которой нужны подсказки:")

    else:
        bot.send_message(message.from_user.id, "Такого студента нет ¯\_(ツ)_/¯  \n"
                                               "Введи другой номер зачетки")

    @bot.message_handler()
    def hints(message):
        data = json.loads(response.text)
        try:

            for i in (data[user]['labs'][message.text]['hints']):
                bot.send_message(message.from_user.id, data[user]['labs'][message.text]['hints'][str(i)])
            bot.send_message(message.from_user.id, "Выбери номер лабораторной по которой нужны подсказки:")

        except:
            bot.send_message(message.from_user.id, "Выбери номер лабораторной по которой нужны подсказки:")


bot.polling(none_stop=True, interval=0)
