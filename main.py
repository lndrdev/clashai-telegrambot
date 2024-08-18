import os
import requests

from dotenv import load_dotenv as ld

from dankware import clr, cls

from collections import deque

import telebot

ld()
BOT_TOKEN = os.getenv('TOKEN')
CLASHAI_API_KEY = os.getenv('CLASHAI_APIKEY')

bot = telebot.TeleBot(BOT_TOKEN)

user_histories = {}

def get_user_history(user_id):
    if user_id not in user_histories:
        user_histories[user_id] = deque(maxlen=15)
    return user_histories[user_id]

@bot.message_handler()
def start(message):
    if message.text == "/start":
        bot.reply_to(message, "⚠️ This bot can access your first and last name to address you personally! ⚠️\n\nTo start, write a message." if message.from_user.language_code == "en" else "⚠️ Dieser Bot kann auf deinen Vor- und Nachnamen zugreifen, um dich persönlich anzusprechen! ⚠️\n\nUm zu starten, schreibe eine Nachricht.")
    else:
        if str(message.text).startswith('.') or str(message.text).startswith("/"):
            return
        jugendlicher = f"""Du bist ein Jugendlicher, der füllwörter wie 'sheesh', 'digga', 'erhaben', usw. benutzt. du benutzt auch emojis in deinen Nachrichten
Nutzer mit welchem du schreibst: {message.from_user.first_name}
Die Sprache des Nutzers ist: {message.from_user.language_code}. Antworte ihm NUR in dieser Srache!"""
        user_history = get_user_history(user_id=message.from_user.id)
        user_history.append({"role": "user", "content": message.text})
        sys_prompt = {"role": "system", "content": jugendlicher}
        url = "http://clashai.3utilities.com:25621/v1/chat/completions"
        payload = {
                "model": "chatgpt-4o-latest",
                "messages": list(user_history) + [sys_prompt] + [{"role": "user", "content": message.text}]
                                                                ,
            }
        headers = {
            "Authorization": f"Bearer {CLASHAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        msg = response.json()['choices'][0]['message']['content']
        bot.reply_to(message, msg)

cls()
banner = """
░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░  ░▒▓█▓▒░     
                                                                                        """
print(clr(banner))
bot.infinity_polling()