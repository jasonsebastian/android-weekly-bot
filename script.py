import asyncio
from bs4 import BeautifulSoup
import requests
from telegram import Bot

URL = "https://androidweekly.net/"
TOKEN = "6828356006:AAFW2u2E5kQ9LTHAGFK06hGJMS_OWNv_awo"
USER_CHAT_ID = "1377504783"


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
    articles = soup.find_all(class_="content-text")
    return list(map(transform, articles))


async def send_async_message(bot, chat_id):
    message = "*Android Weekly*\n\n"
    data = fetch_android_weekly_data()
    for i, d in enumerate(data):
        message += f"{i+1}. [{d['title']}]({d['link']})\n"
        message += d["desc"]
        if i < len(data) - 1:
            message += "\n\n"
    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")


def test_send_message():
    message = "*Android Weekly*\n\n"
    data = fetch_android_weekly_data()
    for i, d in enumerate(data):
        message += f"{i+1}. [{d['title']}]({d['link']})\n"
        message += d["desc"]
        if i < len(data) - 1:
            message += "\n\n"
    print(message)


def send_message_using_bot():
    bot = Bot(TOKEN)
    asyncio.run(send_async_message(bot, USER_CHAT_ID))


send_message_using_bot()