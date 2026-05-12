from http.server import BaseHTTPRequestHandler
import json
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
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

class handler(BaseHTTPRequestHandler):

    # =========================
    # Browser GET request
    # =========================
    def do_GET(self):

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(
            b"Tmail By Eleas Bot Running"
        )

    # =========================
    # Telegram POST webhook
    # =========================
    def do_POST(self):

        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)

        data = json.loads(body)

        message = data.get("message", {})

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

            users[chat_id] = email

            send_message(
                chat_id,
                f"Your Temp Mail:\n\n{email}"
            )

        elif text == "/check":

            if chat_id not in users:

                send_message(
                    chat_id,
                    "Use /newmail first"
                )

            else:

                email = users[chat_id]

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

        self.send_response(200)
        self.end_headers()
