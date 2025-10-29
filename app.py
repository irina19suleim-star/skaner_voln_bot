from flask import Flask, request
import telebot
import os

# Токен берётся из переменных окружения Render
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Основной маршрут (корень) ---
@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        # Приходит обновление от Telegram
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200
    else:
        # Проверка, что сервер запущен
        return "Bot is running 🌊", 200


# --- Команды бота ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я Сканер Души 🌊✨")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, f"Ты написал(а): {message.text}")


# --- Запуск приложения ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
