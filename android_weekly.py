from bs4 import BeautifulSoup
import requests


def fetch_android_weekly_data():
    def transform(article):
        return {
            "title": escape_open_brackets(article.find("a").get_text(strip=True)),
            "link": article.find("a")["href"],
            "desc": article.find(class_="text-container")
            .find("div")
            .contents[1]
            .get_text(strip=True),
        }

    response = requests.get("https://androidweekly.net/")
    if response.status_code != 200:
        print("Failed to retrieve the website")
        return
    soup = BeautifulSoup(response.content, "html.parser")
    edition = (
        soup.find(class_="issue-header").find(class_="clearfix").get_text(strip=True)
    )
    articles = soup.find_all(class_="content-text")
    return edition, list(map(transform, articles))


def get_android_weekly():
    edition, data = fetch_android_weekly_data()
    message = f"*Android Weekly {edition}*\n\n"
    for i, d in enumerate(data):
        message += f"{i+1}. [{d['title']}]({d['link']})\n"
        message += d["desc"]
        if i < len(data) - 1:
            message += "\n\n"
    return message


def escape_open_brackets(text):
    return text.replace("[", r"\[")


if __name__ == "__main__":
    print(get_android_weekly())
