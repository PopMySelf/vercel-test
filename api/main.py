import os
import time
# from threading import Thread
from traceback import format_exc

from flask import Flask, request
from telebot import TeleBot, types

t = time.perf_counter()
app = Flask(__name__)
bot = TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])


@app.post('/')
def handle_telegram():
    if request.content_type == 'application/json' and (
            update := types.Update.de_json(request.stream.read().decode('utf-8'))
    ).message and update.message.from_user.id in [652015662]:
        bot.send_message(
            652015662,
            f'{type(update.message.from_user.id)}\n{time.perf_counter() - t = }',
            timeout=5
        )
        bot.process_new_updates([update])

    return ''


@bot.message_handler()
def handle(m: types.Message):
    try:
        bot.send_message(m.chat.id, f'{time.perf_counter() - t = }', timeout=5)
    except Exception:
        bot.send_message(m.chat.id, format_exc())


