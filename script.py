import asyncio
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests
from telegram import Bot

load_dotenv()

URL = "https://androidweekly.net/"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USER_CHAT_ID = os.getenv("TELEGRAM_USER_ID")


def fetch_android_weekly_data():
    def transform(article):
        return {
            "title": article.find("a").get_text(strip=True),
            "link": article.find("a")["href"],
            "desc": article.find(class_="text-container")
            .find("div")
            .contents[1]
            .get_text(strip=True),
        }

    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to retrieve the website")
        return
    soup = BeautifulSoup(response.content, "html.parser")
    edition = (
        soup.find(class_="issue-header").find(class_="clearfix").get_text(strip=True)
    )
    articles = soup.find_all(class_="content-text")
    return edition, list(map(transform, articles))


def get_message():
    edition, data = fetch_android_weekly_data()
    message = f"*Android Weekly {edition}*\n\n"
    for i, d in enumerate(data):
        message += f"{i+1}. [{d['title']}]({d['link']})\n"
        message += d["desc"]
        if i < len(data) - 1:
            message += "\n\n"
    return message


async def send_async_message(bot, chat_id):
    await bot.send_message(chat_id=chat_id, text=get_message(), parse_mode="Markdown")


def test_send_message():
    print(get_message())


def send_message_using_bot():
    bot = Bot(TOKEN)
    asyncio.run(send_async_message(bot, USER_CHAT_ID))


send_message_using_bot()
