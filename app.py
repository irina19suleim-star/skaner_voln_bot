import os
import threading
from flask import Flask

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

# --- HTTP healthcheck для Render ---
@app.route("/")
def health():
    return "OK", 200

# --- Handlers Telegram ---
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я «Сканер души». Я на связи и готов отвечать 🌿"
    )

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if text.lower() in {"привет", "hi", "hello"}:
        await update.message.reply_text("Привет-привет! ✨")
    else:
        await update.message.reply_text("Я услышал тебя. Команда: /start")

def run_bot():
    if not BOT_TOKEN:
        print("❗BOT_TOKEN не задан. Проверь переменные окружения на Render.")
        return
    app_ = Application.builder().token(BOT_TOKEN).build()
    app_.add_handler(CommandHandler("start", cmd_start))
    app_.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    # long-polling
    app_.run_polling(allowed_updates=Update.ALL_TYPES)

# Запускаем polling в фоне, а Flask оставляем для Render
_bot_started = False
@app.before_first_request
def activate_bot():
    global _bot_started
    if not _bot_started:
        t = threading.Thread(target=run_bot, daemon=True)
        t.start()
        _bot_started = True

if __name__ == "__main__":
    # локальный запуск
    port = int(os.environ.get("PORT", 10000))
    activate_bot()
    app.run(host="0.0.0.0", port=port)
