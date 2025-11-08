import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_user_by_username(username):
    """Проверяет существование пользователя по username"""
    # Убираем @ если есть
    username = username.lstrip('@')
    
    url = f"https://t.me/{username}"
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            if "tgme_username" in response.text:
                return True, "существует ✅"
        return False, "не найден ❌"
    except Exception as e:
        logger.error(f"Ошибка при проверке {username}: {e}")
        return False, f"ошибка проверки: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для проверки пользователей Telegram.\n"
        "Отправь мне username (например: @durov или просто durov)"
    )

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_input = update.message.text.strip()
    
    if not user_input:
        await update.message.reply_text("Пожалуйста, отправь username")
        return
    
    # Показываем что бот работает
    processing_msg = await update.message.reply_text("🔍 Проверяю...")
    
    # Проверяем пользователя
    exists, status = check_user_by_username(user_input)
    
    # Формируем ответ
    username_clean = user_input.lstrip('@')
    response_text = f"👤 Пользователь @{username_clean}\nСтатус: {status}"
    
    # Обновляем сообщение с результатом
    await context.bot.edit_message_text(
        chat_id=update.message.chat_id,
        message_id=processing_msg.message_id,
        text=response_text
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "ℹ️ **Как пользоваться ботом:**\n\n"
        "Просто отправь мне username пользователя:\n"
        "• `@username`\n"
        "• `username`\n\n"
        "Примеры:\n"
        "• `@durov`\n"
        "• `telegram`\n\n"
        "Я проверю, существует ли такой пользователь в Telegram.",
        parse_mode='Markdown'
    )

def main():
    """Запуск бота"""
    # Токен бота от @BotFather
    TOKEN = "8259782982:AAF_cCRncLPaM2X5KViHg7PF3Vu8lqk1kCA"
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user))
    
    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()