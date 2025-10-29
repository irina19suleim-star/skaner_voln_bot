# app.py
# Telegram-бот на Flask + вебхук для Render
# Работает с переменными окружения:
#   BOT_TOKEN            — токен бота от @BotFather (обязательно)
#   PUBLIC_URL (опц.)    — публичный URL сервиса (например https://skaner-voln-bot.onrender.com)
# Render обычно сам даёт RENDER_EXTERNAL_URL — мы тоже его используем.

import os
from flask import Flask, request
import telebot

# === 1) Конфиг ===
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Переменная окружения BOT_TOKEN не задана")

# Пытаемся взять публичный URL из PUBLIC_URL или из системной RENDER_EXTERNAL_URL
PUBLIC_URL = os.getenv("PUBLIC_URL") or os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# === 2) Хэндлеры бота ===
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я Сканер Души 🌊✨\nНапиши мне что-нибудь — я отвечу."
    )

@bot.message_handler(func=lambda m: True)
def handle_echo(message):
    bot.send_message(message.chat.id, f"Ты написал(а): <b>{message.text}</b>")

# === 3) Вебхук ===
@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    try:
        data = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return "ok", 200
    except Exception as e:
        # В логах Render увидишь ошибку, если что-то пойдёт не так
        print("WEBHOOK ERROR:", repr(e))
        return "error", 500

# Простой пинг, чтобы видеть, что сервис жив
@app.route("/", methods=["GET"])
def root():
    return "Bot is running 🏄", 200

# === 4) Установка вебхука при старте (если знаем публичный URL) ===
def ensure_webhook():
    try:
        if not PUBLIC_URL:
            print("PUBLIC_URL/RENDER_EXTERNAL_URL не задан — вебхук не устанавливаем.")
            return
        url = PUBLIC_URL.rstrip("/") + "/webhook"
        current = bot.get_webhook_info().url
        if current != url:
            bot.remove_webhook()
            bot.set_webhook(url=url, max_connections=40)
            print(f"Webhook set to: {url}")
        else:
            print(f"Webhook already set: {url}")
    except Exception as e:
        print("SET WEBHOOK ERROR:", repr(e))

# === 5) Точка входа ===
if __name__ == "__main__":
    ensure_webhook()
    port = int(os.getenv("PORT", "10000"))  # Render слушает этот порт
    app.run(host="0.0.0.0", port=port)
