from flask import Flask, request
import telebot
import os
import json

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# health-check, чтобы корень открывался
@app.route("/", methods=["GET"])
def index():
    return "Bot is running 🏄", 200

# вебхук — сюда Telegram шлёт апдейты
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return "ok", 200
    except Exception as e:
        # поможет увидеть ошибку в логах Render
        print("WEBHOOK ERROR:", e)
        return "error", 500

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я Сканер Души 🌊✨")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, f"Ты написал(а): {message.text}")

if __name__ == "__main__":
    # Render слушает порт из переменной среды; у тебя это 10000 — тоже ок.
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)

    app.run(host="0.0.0.0", port=port)
