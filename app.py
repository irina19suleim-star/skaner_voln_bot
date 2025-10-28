from flask import Flask, request
import os
import telebot

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # https://skaner-voln-bot.onrender.com/webhook/<ТОКЕН>

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")
bot = telebot.TeleBot(BOT_TOKEN)

@app.route("/", methods=["GET"])
def index():
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return "healthy", 200

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    upd = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([upd])
    return "", 200

@bot.message_handler(commands=["start"])
def handle_start(msg):
    bot.reply_to(msg, "Привет 🌿 Я запущен!")

# Настраиваем webhook перед первым запросом (при старте инстанса)
@app.before_first_request
def setup_webhook():
    if WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
