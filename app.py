# app.py
import os
from flask import Flask, request, abort
import telebot

TOKEN = os.environ["BOT_TOKEN"]  # переменная в Render -> Environment -> BOT_TOKEN
bot = telebot.TeleBot(TOKEN, threaded=False, parse_mode="HTML")

app = Flask(__name__)

@app.get("/")
def index():
    return "Bot is running 🌊", 200

@app.post("/webhook")
def telegram_webhook():
    # Telegram всегда шлёт JSON; нужно передать ЕГО, а не строку, в de_json
    if request.headers.get("content-type") != "application/json":
        abort(403)

    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200


# ====== Handlers ======
@bot.message_handler(commands=["start"])
def on_start(message):
    bot.send_message(message.chat.id, "Привет! Я Сканер Души 🌊✨")

@bot.message_handler(content_types=["text"])
def echo(message):
    bot.send_message(message.chat.id, f"Ты написала: <b>{message.text}</b>")

# локальный запуск (Render всё равно поднимет через gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
