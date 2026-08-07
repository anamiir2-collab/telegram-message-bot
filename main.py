import requests
import json
from datetime import datetime

BOT_TOKEN = "YOUR_BOT_TOKEN"  # ضع التوكن هنا

# قائمة الـ user IDs
USER_IDS = [123456789, 987654321, 111222333]

def send_to_all(message):
    """إرسال رسالة لكل الناس"""
    for user_id in USER_IDS:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": user_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data)
            print(f"✅ تم الإرسال للـ {user_id}")
        except Exception as e:
            print(f"❌ خطأ في الإرسال للـ {user_id}: {e}")

def load_messages():
    """تحميل الرسائل من messages.txt"""
    try:
        with open('messages.txt', 'r', encoding='utf-8') as f:
            return f.readlines()
    except:
        return []

if __name__ == "__main__":
    messages = load_messages()
    
    if messages:
        message = messages[0].strip()  # أول رسالة
        print(f"📤 إرسال: {message}")
        send_to_all(message)
    else:
        print("لا توجد رسائل!")
