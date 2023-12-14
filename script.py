import asyncio
from dotenv import load_dotenv
import os
from telegram import Bot

from android_weekly import get_android_weekly
from subscription import get_subscribers_list

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def send_async_message(bot, chat_id):
    await bot.send_message(
        chat_id=chat_id, text=get_android_weekly(), parse_mode="Markdown"
    )


if __name__ == "__main__":
    bot = Bot(TELEGRAM_BOT_TOKEN)
    subscribers = get_subscribers_list()
    if subscribers is not None:
        for user_id in subscribers:
            asyncio.run(send_async_message(bot, user_id))
