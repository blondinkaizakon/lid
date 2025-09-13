import os
import asyncio
import logging
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# === Настройки ===
CHANNEL_ID = -100246645098
DOWNLOAD_LINK = 'https://disk.yandex.ru/i/5qJyHoKiMonmPw'
WEBHOOK_URL = f"https://blondinkaizakon-lid-f051.twc1.net/{BOT_TOKEN}"
PORT = int(os.environ.get("PORT", 8000))

SUCCESS_MESSAGE = (
    "✅ Вы подписаны!\n\n"
    "Откройте материал по ссылке:\n"
    f"{DOWNLOAD_LINK}\n\n"
    "👉 Скопируйте ссылку и вставьте в браузер."
)

logging.basicConfig(level=logging.INFO)
app_fastapi = FastAPI()
app_telegram = Application.builder().token(BOT_TOKEN).build()

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Подпишитесь на канал и нажмите кнопку ниже.",
        reply_markup=reply_markup
    )

# === Проверка подписки ===
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    try:
        member = await app_telegram.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
        if member.status in ['member', 'administrator', 'creator']:
            await query.edit_message_text(SUCCESS_MESSAGE)
        else:
            keyboard = [[InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ Вы не подписаны на канал.\nПодпишитесь и попробуйте снова.",
                reply_markup=reply_markup
            )
    except Exception as e:
        await query.edit_message_text("❌ Ошибка проверки подписки.")

# === Telegram handlers ===
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))

# === FastAPI ===
@app_fastapi.get("/")
def read_root():
    return {"status": "ok"}

@app_fastapi.post(f"/{BOT_TOKEN}")
async def webhook(update: dict):
    await app_telegram.initialize()
    await app_telegram.process_update(Update.de_json(update, app_telegram.bot))
    return {"ok": True}

# === Запуск ===
async def run_bot():
    await app_telegram.initialize()
    await app_telegram.start()
    await app_telegram.bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    asyncio.run(run_bot())
    import uvicorn
    uvicorn.run(app_fastapi, host="0.0.0.0", port=PORT)
