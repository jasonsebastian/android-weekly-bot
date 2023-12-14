import json

from gists import get_gist_content, update_gist


def subscribe(user_id):
    subscribers = get_subscribers_list()
    if subscribers is not None:
        if user_id not in subscribers:
            subscribers.append(user_id)
            updated_content = json.dumps(subscribers, indent=4)

            if update_gist(updated_content):
                return "You are now subscribed."
            else:
                return "Failed to subscribe."
        else:
            return "You are already subscribed."
    else:
        return "Failed to fetch subscriber list."


def unsubscribe(user_id):
    subscribers = get_subscribers_list()
    if subscribers is not None:
        if user_id in subscribers:
            subscribers.remove(user_id)
            updated_content = json.dumps(subscribers)

            if update_gist(updated_content):
                return "You are now unsubscribed."
            else:
                return "Failed to unsubscribe."
        else:
            return "You are not subscribed."
    else:
        return "Failed to fetch subscriber list."


def get_subscribers_list():
    content = get_gist_content()
    if content is not None:
        subscribers = json.loads(content)
        return subscribers
    else:
        return None


if __name__ == "__main__":
    message = get_subscribers_list()
    print(message)
