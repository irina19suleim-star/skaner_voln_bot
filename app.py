import os
import threading
import logging
from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("Привет 💫 Я бот проекта Волновой Сканер Души. Готов к работе!")

def echo(update, context):
    update.message.reply_text(update.message.text)

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

app = Flask(__name__)

@app.route("/")
def index():
    return "Бот запущен и слушает поток 🌊", 200

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
