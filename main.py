import os
import random
import telebot

# جلب البيانات من الـ Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)

def send_random_message():
    # قراءة الرسائل من ملف messages.txt
    if os.path.exists('messages.txt'):
        with open('messages.txt', 'r', encoding='utf-8') as f:
            messages = [line.strip() for line in f if line.strip()]
        
        if messages:
            random_msg = random.choice(messages)
            bot.send_message(CHAT_ID, random_msg)
            print("Message sent successfully!")
        else:
            print("messages.txt is empty.")
    else:
        print("messages.txt file not found.")

if __name__ == '__main__':
    send_random_message()
