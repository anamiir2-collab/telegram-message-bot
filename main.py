import os
import random
import requests

# جلب البيانات من الـ Secrets
token = os.environ.get("BOT_TOKEN")
chat_id = os.environ.get("CHAT_ID")

# قراءة الرسائل من ملف messages.txt
with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f if line.strip()]

# اختيار رسالة عشوائية وإرسالها
if messages and token and chat_id:
    message = random.choice(messages)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, json=payload)
