from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = "8259782982:AAF_cCRncLPaM2X5KViHg7PF3Vu8lqk1kCA"

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Напиши: /check @username")
    
    username = context.args[0].replace("@", "")

    try:
        user = await context.bot.get_chat(username)
        await update.message.reply_text(f"✅ Пользователь существует!\nID: `{user.id}`", parse_mode="Markdown")

    except BadRequest as e:
        if "not found" in str(e).lower():
            await update.message.reply_text("❌ Такой пользователь НЕ существует!")
        else:
            await update.message.reply_text(f"⚠️ Ошибка: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("check", check))
    app.run_polling()

if __name__ == "__main__":
    main()
