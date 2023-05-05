import requests
import json

class DiscordWebhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.headers = {
            "Content-Type": "application/json"
        }

    def send_message(self, content):
        payload = {
            "content": content
        }

        response = requests.post(self.webhook_url, data=json.dumps(payload), headers=self.headers)

        if response.status_code == 204:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response.text)

# if __name__ == "__main__":
#     webhook_url = "YOUR_WEBHOOK_URL"  # Replace this with your webhook URL
#     message_content = "Hello, Discord!"  # Replace this with the message you want to send

#     discord_webhook = DiscordWebhook(webhook_url)
#     discord_webhook.send_message(message_content, username="MyBot", avatar_url=None)
