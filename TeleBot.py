from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json
import requests


response = requests.get('http://taskbotsibadi.us.aldryn.io/bot/json_response')
data = json.loads(response.text)



def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет студент, введи свой номер заченой книжки =).\nПример: bi20in, где n твой номер в '
                              'списке.')


def hints(update: Update, context: CallbackContext):
    response = requests.get('http://taskbotsibadi.us.aldryn.io/bot/json_response')
    data = json.loads(response.text)
    try:

        for i in (data[user]['labs'][update.message.text]['hints']):
            update.message.reply_text(data[user]['labs'][update.message.text]['hints'][str(i)])
        update.message.reply_text("Выбери номер лабораторной по которой нужны подсказки:")

    except:
        update.message.reply_text("Подсказок нет =( \nИли вы не ввели номер зачетной книжки ¯\_(ツ)_/¯")


def say(update: Update, context: CallbackContext):
    response = requests.get('http://taskbotsibadi.us.aldryn.io/bot/json_response')
    data = json.loads(response.text)
    global user
    user = update.message.text.lower()
    if user in data:
        sum_labs = 0

        update.message.reply_text(data[user]['name'])
        for lab in data[user]['labs']:
            if data[user]['labs'][lab]['status'] == 0:
                sum_labs += 1
                update.message.reply_text('%s\n%s\n%s' % ("Номер лабы: " + str(lab),
                                                          "Назавание лабы: " + data[user]['labs'][lab]['name'],
                                                          "Задание: " + data[user]['labs'][lab]['description']))
        if sum_labs > 0:
            update.message.reply_text("Выбери номер лабораторной по которой нужны подсказки:")
    else:
        update.message.reply_text("Такого студента нет ¯\_(ツ)_/¯  \nВведи другой номер зачетки")


# def hints(update: Update, context: CallbackContext):


def main():
    updater = Updater(token='1148909884:AAFywUYIklb21bfeGKb8gEnp8P-1Bivdf6A', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    text_handler = MessageHandler(Filters.regex("bi20i"), say)
    Hints_handler = MessageHandler(Filters.text, hints)
    dp.add_handler(text_handler)
    dp.add_handler(Hints_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
