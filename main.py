import os
import logging
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

TOKEN = '7847097021:AAHJ3Ij4Gu12BZAkjMzSeLWyYDdkwuLf4rU'
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = f"https://your-app-112381.timeweb.app/{TOKEN}"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот запущен и работает через вебхук!")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        url_path=TOKEN,
    )
