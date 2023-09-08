import os
import time
# from threading import Thread
from traceback import format_exc

import pyrogram
from flask import Flask, request
from telebot import TeleBot, types

t = time.perf_counter()
app = Flask(__name__)
bot = TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])

c = None


@app.post('/')
def handle_telegram():
    if request.content_type == 'application/json' and (
            update := types.Update.de_json(request.stream.read().decode('utf-8'))
    ).message and update.message.from_user.id in [652015662]:
        handle(update.message)
        # bot.process_new_updates([update])

    return ''


# @bot.message_handler()
def handle(m: types.Message):
    try:
        bot.send_message(
            m.chat.id,
            f'{time.perf_counter() - t = }\n\n'
        )
        if not c or not c.is_connected:
            bot.send_message(m.chat.id, 'running that...')
            userbot_functionality()

    except Exception:
        bot.send_message(
            m.chat.id,
            f'{time.perf_counter() - t = }\n\nAn ERROR occurred:\n\n{format_exc()}'
        )


def userbot_functionality() -> str:
    global c

    try:
        c = pyrogram.Client(
            'make_voices_louder',
            session_string=os.environ['TGSS']
        )

        r = None

        # @app.on_message(pyrogram.filters.voice & pyrogram.filters.chat())
        @c.on_message()
        async def handle_normalize_audio(client: pyrogram.Client, m: pyrogram.types.Message):
            # await client.send_voice(
            #     m.chat.id,
            #     normalize_audio(
            #         await client.download_media(m, in_memory=True).getvalue()
            #     )
            # )
            nonlocal r
            r = m.forward('me')
            await client.disconnect()

        c.run()
        return str(r)

    except Exception:
        return format_exc()

