import os
from threading import Thread

from flask import Flask, request
from telebot import TeleBot, types

app = Flask(__name__)
bot = TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
#

@app.get('/')
def me():
    return os.environ['VERCEL_ENV']


@app.post('/')
def handle_telegram():
    if request.content_type == 'application/json' and (
            update := types.Update.de_json(request.stream.read().decode('utf-8'))
    ).message and update.message.from_user.id in [652015662]:
        thread = Thread(target=bot.process_new_updates, args=([update],))
        thread.start()

    return ''


@bot.message_handler(commands=['tv'])
def handle_tv(m: types.Message):
    bot.send_message(m.chat.id, f'{os.environ["VERCEL_ENV"]}')


