# app.py
# ----------------------------
# Flask + pyTelegramBotAPI (telebot)
# Вебхук для Render: /webhook
# Требует переменную окружения BOT_TOKEN

import os
import logging
from flask import Flask, request, jsonify
import telebot

# ---------- Логирование ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("skaner_voln_bot")

# ---------- Токен ----------
TOKEN = os.environ.get("BOT_TOKEN", "").strip()
if not TOKEN:
    # Упадём сразу, чтобы не ловить 404 от Telegram позже
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения Render")

# ---------- Бот ----------
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Проверим соединение с Telegram на старте
try:
    me = bot.get_me()
    log.info(f"Connected to Telegram as @{me.username} (id={me.id})")
except Exception as e:
    # Если сюда попали — токен битый или сеть недоступна
    log.exception("Telegram getMe failed: %s", e)
    raise

# ---------- Flask ----------
app = Flask(__name__)

@app.get("/")
def root():
    # healthcheck для Render
    return "Bot is running 🏄‍♀️", 200

@app.post("/webhook")
def telegram_webhook():
    # Telegram присылает JSON Update
    try:
        json_str = request.get_data(as_text=True)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    except Exception as e:
        log.exception("Webhook handling error: %s", e)
        return "error", 500
    return "ok", 200

# ---------- Хендлеры бота ----------
@bot.message_handler(commands=["start", "help"])
def on_start(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        "Привет! Я Сканер Души 🌊✨\nНапиши что-нибудь — я отвечу."
    )

@bot.message_handler(func=lambda m: True)
def on_echo(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Ты написала: <b>{message.text}</b>")

# ---------- Запуск локально (Render сам запустит через gunicorn) ----------
if __name__ == "__main__":
    # локально: python app.py
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
