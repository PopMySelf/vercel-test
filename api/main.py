import os
import time
from traceback import format_exc

import pyrogram
from flask import Flask
from telebot import TeleBot

t = time.perf_counter()
app = Flask(__name__)
bot = TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])

c = None


def log(text: str, error: bool = False):
    if error:
        text = 'An ERROR occurred:\n\n' + text.replace('<', '^').replace('>', '^')

    bot.send_message(652015662, text)


@app.post('/')
def handle_run():
    if not (c and c.is_connected):
        log('Calling userbot_functionality...')
        userbot_functionality()
        log('This is it, the call has been performed')
    else:
        log(f'Looks like c was already fine.\n{c = }\n{c.is_connected = }')
    return ''


def userbot_functionality():
    try:
        global c

        c = pyrogram.Client(
            'make_voices_louder',
            session_string=os.environ['TGSS']
        )

        @c.on_message()
        async def handle_normalize_audio(client: pyrogram.Client, m: pyrogram.types.Message):
            await client.send_message(
                'me',
                f'{time.perf_counter() - t}\n\n'
                f'handled a message from\n{str(m.chat)}'
            )

        c.run()

    except Exception:
        log(format_exc(), error=True)

