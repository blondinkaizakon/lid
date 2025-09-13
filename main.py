import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# === Настройки ===
BOT_TOKEN = '7847097021:AAHJ3Ij4Gu12BZAkjMzSeLWyYDdkwuLf4rU'
CHANNEL_ID = -246645098  # 
DOWNLOAD_LINK = 'https://disk.yandex.ru/i/5qJyHoKiMonmPw'
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = f"https://your-app-12345.timeweb.app/{BOT_TOKEN}"

SUCCESS_MESSAGE = (
    "✅ Вы подписаны!\n\n"
    "Откройте материал по ссылке:\n"
    f"{DOWNLOAD_LINK}\n\n"
    "👉 Скопируйте ссылку и вставьте в браузер."
)

# === Логирование ===
logging.basicConfig(level=logging.INFO)

# === Хэндлеры ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Подпишитесь на канал и нажмите кнопку ниже.",
        reply_markup=reply_markup
    )

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
        if member.status in ['member', 'administrator', 'creator']:
            await query.edit_message_text(SUCCESS_MESSAGE)
        else:
            keyboard = [[InlineKeyboardButton("Проверить подписку", callback_data="check_subscription")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("❌ Вы не подписаны.", reply_markup=reply_markup)
    except Exception as e:
        await query.edit_message_text("❌ Ошибка проверки подписки.")

# === Приложение ===
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))

# === Запуск ===
if __name__ == '__main__':
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        url_path=BOT_TOKEN,
    )
