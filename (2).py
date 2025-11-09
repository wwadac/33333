import os
import aiohttp
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ТОЛЬКО токен бота
BOT_TOKEN = os.getenv('8259782982:AAF_cCRncLPaM2X5KViHg7PF3Vu8lqk1kCA')

async def check_user_via_web(username):
    """Проверяем пользователя через веб-интерфейс Telegram"""
    try:
        # Убираем @ если есть
        if username.startswith('@'):
            username = username[1:]
        
        # Пробуем получить страницу пользователя
        url = f"https://t.me/{username}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                # Если страница существует и не редиректит на ошибку
                if response.status == 200:
                    html = await response.text()
                    
                    # Проверяем типичные признаки существующего пользователя
                    if 'tgme_page_extra' in html or 'tgme_username' in html:
                        return {'exists': True, 'username': username}
                    elif 'If you have <strong>Telegram</strong>' in html:
                        return {'exists': False}
                    else:
                        # Если не можем определить - считаем что существует
                        return {'exists': True, 'username': username}
                else:
                    return {'exists': False}
                    
    except Exception as e:
        return {'exists': False, 'error': str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 **Проверка пользователей Telegram**\n\n"
        "Отправь мне username (например: @username) и я проверю его существование!\n\n"
        "Работает через веб-версию Telegram - никаких API ключей не нужно!"
    )

async def check_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    
    if not username:
        await update.message.reply_text("❌ Отправь username пользователя")
        return
    
    processing_msg = await update.message.reply_text("🔍 Проверяю...")
    
    try:
        result = await check_user_via_web(username)
        
        if result['exists']:
            await processing_msg.edit_text(
                f"✅ **Пользователь найден!**\n\n"
                f"👤 Username: @{result['username']}\n"
                f"🌐 Ссылка: https://t.me/{result['username']}"
            )
        else:
            await processing_msg.edit_text(
                f"❌ **Пользователь не найден**\n\n"
                f"Username: @{username.replace('@', '')}\n"
                f"Такого пользователя не существует или username неправильный."
            )
            
    except Exception as e:
        await processing_msg.edit_text(f"⚠️ Ошибка: {str(e)}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_user_handler))
    
    print("Бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
