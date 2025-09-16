import asyncio
import uvicorn
from fastapi import FastAPI
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from threading import Thread

# FastAPI приложение
app_fastapi = FastAPI()

@app_fastapi.get("/")
def read_root():
    return {"status": "ok"}

@app_fastapi.post("/webhook")
async def webhook(update: dict):
    # Обработка вебхука
    return {"ok": True}

# Telegram бот
async def start(update, context):
    keyboard = [[InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Подпишитесь на канал и нажмите кнопку ниже.",
        reply_markup=reply_markup
    )

async def check_subscription(update, context):
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

# Инициализация Telegram бота
app_telegram = Application.builder().token(BOT_TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))

# Запуск Telegram бота в отдельном потоке
def run_telegram_bot():
    app_telegram.run_polling()

# Запуск Telegram бота в отдельном потоке
telegram_thread = Thread(target=run_telegram_bot)
telegram_thread.start()

# Запуск FastAPI приложения с помощью Uvicorn
if __name__ == "__main__":
    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)
