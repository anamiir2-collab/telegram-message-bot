import os
import random
import sys
import requests

# جلب البيانات من الـ Secrets
token = os.environ.get("BOT_TOKEN")
chat_id = os.environ.get("CHAT_ID")

if not token or not chat_id:
    print("خطأ: BOT_TOKEN أو CHAT_ID مش متظبطين في الـ Secrets.")
    sys.exit(1)

# قراءة الرسائل من ملف messages.txt
with open("messages.txt", "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f if line.strip()]

if not messages:
    print("خطأ: ملف messages.txt فاضي.")
    sys.exit(1)

# اختيار رسالة عشوائية وإرسالها
message = random.choice(messages)
url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {"chat_id": chat_id, "text": message}

response = requests.post(url, json=payload, timeout=15)

if response.status_code == 200:
    print(f"تم إرسال الرسالة بنجاح: {message}")
else:
    print(f"فشل الإرسال. الحالة: {response.status_code}, الرد: {response.text}")
    sys.exit(1)
