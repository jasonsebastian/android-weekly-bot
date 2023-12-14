from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler

from subscription import subscribe, unsubscribe

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def subscribe_handler(update, context):
    user_id = str(update.message.chat_id)
    message = subscribe(user_id)
    await update.message.reply_text(message)


async def unsubscribe_handler(update, context):
    user_id = str(update.message.chat_id)
    message = unsubscribe(user_id)
    await update.message.reply_text(message)


if __name__ == "__main__":
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("subscribe", subscribe_handler))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_handler))
    application.run_polling()
