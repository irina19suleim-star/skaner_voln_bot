import os
from flask import Flask, request
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Нет переменной окружения BOT_TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# healthcheck
@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

# Telegram шлёт апдейты сюда
@app.route(f"/{TOKEN}", methods=["POST"])
def tg_webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

# хендлеры
@bot.message_handler(commands=["start", "help"])
def cmd_start(msg):
    bot.reply_to(msg, "Я на связи. Напиши любое слово — отвечу 😉")

@bot.message_handler(func=lambda m: True)
def echo(msg):
    bot.reply_to(msg, f"Ты написал(а): <b>{msg.text}</b>")

def setup_webhook():
    # Render сам даёт внешний URL в переменной RENDER_EXTERNAL_URL
    base = os.environ.get("RENDER_EXTERNAL_URL")
    if base:
        url = f"{base}/{TOKEN}"
        try:
            bot.remove_webhook()
        finally:
            bot.set_webhook(url=url)
        print("Webhook set to:", url)
    else:
        print("RENDER_EXTERNAL_URL не найден — вебхук не выставлен")

setup_webhook()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
