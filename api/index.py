import json
import requests

BOT_TOKEN = "8652494574:AAF5NMh97pPBsohZfBXFbOZwtAdJHmbtqrw"

API = f"https://api.telegram.org/bot{BOT_TOKEN}/"

users = {}

def send_message(chat_id, text):

    requests.post(
        API + "sendMessage",
        data={
            "chat_id": chat_id,
            "text": text
        }
    )

def generate_mail():

    url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"

    return requests.get(url).json()[0]

def handler(request):

    # Browser test
    if request.method == "GET":

        return {
            "statusCode": 200,
            "body": "Tmail By Eleas Running"
        }

    # Telegram webhook
    body = json.loads(request.body)

    message = body.get("message", {})

    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text == "/start":

        send_message(
            chat_id,
            "Tmail By Eleas\n\n"
            "/newmail\n"
            "/check"
        )

    elif text == "/newmail":

        email = generate_mail()

        users[str(chat_id)] = email

        send_message(
            chat_id,
            f"Your Temp Mail:\n\n{email}"
        )

    elif text == "/check":

        if str(chat_id) not in users:

            send_message(
                chat_id,
                "Use /newmail first"
            )

        else:

            email = users[str(chat_id)]

            login, domain = email.split("@")

            url = (
                "https://www.1secmail.com/api/v1/"
                f"?action=getMessages&login={login}&domain={domain}"
            )

            msgs = requests.get(url).json()

            if not msgs:

                send_message(
                    chat_id,
                    "Inbox Empty"
                )

            else:

                txt = ""

                for m in msgs:

                    txt += (
                        f"From: {m['from']}\n"
                        f"Subject: {m['subject']}\n\n"
                    )

                send_message(chat_id, txt)

    return {
        "statusCode": 200,
        "body": "ok"
    }
