import os
from flask import Flask, request, abort
import telebot

TOKEN = os.environ.get("BOT_TOKEN", "").strip()  # без пробелов/кавычек!
if not TOKEN:
    raise RuntimeError("BOT_TOKEN отсутствует в переменных окружения")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# 1) Простой корень — чтобы Render видел «живой» сервис
@app.get("/")
def index():
    return "OK", 200

# 2) Вебхук-эндпоинт — сюда Telegram будет слать обновления
@app.post("/webhook")
def tg_webhook():
    if request.headers.get('content-type') != 'application/json':
        abort(403)
    update = request.get_data().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

# 3) Никаких обращений к Telegram при импорте/старте!
#    Хэндлеры ниже — они «спят», пока не придёт апдейт от вебхука.

@bot.message_handler(commands=['start'])
def start_handler(m):
    bot.send_message(m.chat.id, "Привет! Я на связи ✨")

# Gunicorn будет искать переменную app
# if __name__ == "__main__":    # локально — по желанию
#     app.run(host="0.0.0.0", port=8000)
