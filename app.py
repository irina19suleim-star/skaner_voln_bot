import os
from flask import Flask, request, abort
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN env var is not set")

# Один поток, чтобы не было гонок в бесплатном инстансе
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- HTTP-маршруты (Render будет стучаться сюда) ---

@app.get("/")
def index():
    return "OK skaner_voln_bot", 200

@app.post(f"/{TOKEN}")
def telegram_webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
        bot.process_new_updates([update])
        return "!", 200
    abort(403)

# --- Хендлеры бота ---

@bot.message_handler(commands=["start", "help"])
def start(m):
    bot.send_message(m.chat.id, "Привет! Я на Render и уже работаю 🔮")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.send_message(m.chat.id, "Принято: " + m.text)

# --- Включаем веб-хук при старте веб-приложения ---
@app.before_first_request
def setup_webhook():
    base = os.environ.get("RENDER_EXTERNAL_URL", "https://skaner-voln-bot.onrender.com").rstrip("/")
    bot.remove_webhook()
    bot.set_webhook(url=f"{base}/{TOKEN}")
