from flask import Flask, request
import telebot
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def index():
    return "OK"

@app.route(f'/webhook/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 🌸, я жив!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
fix root route
