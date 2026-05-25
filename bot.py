from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from logic import get_ai_response
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hail, traveler! I am thy faithful servant, Sir Qwen. Command me, and I shall answer whatever thou desirest to know.")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Mostra lo stato "sta scrivendo..."
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Usa la logica testata
    answer = get_ai_response(user_text)
    
    await update.message.reply_text(answer)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Bot in ascolto...")
    app.run_polling()