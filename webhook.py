from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from logic import get_ai_response
import os
from dotenv import load_dotenv
from aiohttp import web
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hail, traveler! I am thy faithful servant, Sir Qwen. Command me, and I shall answer whatever thou desirest to know.")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    answer = get_ai_response(user_text)
    await update.message.reply_text(answer)

async def handle_root(request):
    return web.Response(text="OK")

async def handle_webhook(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return web.Response(text="OK")

async def on_startup(app_):
    await app.bot.set_webhook(full_webhook_url)

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    port = int(os.getenv("PORT", "8080"))
    WEBHOOK_BASE = os.getenv("WEBHOOK_BASE")
    if not WEBHOOK_BASE:
        print("Environment variable WEBHOOK_BASE not set. Set it to your service URL (https://...).")
        raise SystemExit(1)

    webhook_path = f"/webhook/{TOKEN}"
    full_webhook_url = WEBHOOK_BASE.rstrip("/") + webhook_path

    web_app = web.Application()
    web_app.add_routes([
        web.get('/', handle_root),
        web.get('/health', handle_root),
        web.post(webhook_path, handle_webhook),
    ])

    print(f"Starting webhook server on port {port}, setting webhook to {full_webhook_url}")

    web_app.on_startup.append(on_startup)

    web.run_app(web_app, host='0.0.0.0', port=port)
