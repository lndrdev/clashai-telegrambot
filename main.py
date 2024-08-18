import os

import clashai

from dotenv import load_dotenv as ld

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
        # #################################################################################################################### #
        jugendlicher = f"""Du bist ein Jugendlicher, der füllwörter wie 'sheesh', 'digga', 'erhaben', usw. benutzt. du benutzt auch emojis in deinen Nachrichten
Nutzer mit welchem du schreibst: {message.from_user.first_name}
Die Sprache des Nutzers ist: {message.from_user.language_code}. Antworte ihm NUR in dieser Srache!
Weitere Infos: Du bist ein Telegram Bot, der Anfragen an die ClashAI API sendet. ClashAI Discord Link: https://discord.gg/ESfE6uRZsV"""
        # #################################################################################################################### #
        user_history = get_user_history(user_id=message.from_user.id)
        user_history.append({"role": "user", "content": message.text})
        # #################################################################################################################### #
        sys_prompt = {"role": "system", "content": jugendlicher}
        # #################################################################################################################### #
        client = clashai.Client(
            api_key=CLASHAI_API_KEY
        )
        # #################################################################################################################### #
        response = client.make_request(
            list(user_history) + [sys_prompt] + [{"role": "user", "content": message.text}]
        )
        # #################################################################################################################### #
        msg = response['choices'][0]['message']['content']
        # #################################################################################################################### #
        bot.reply_to(message, msg, parse_mode='Markdown')

if os.name == 'nt':
    os.system('cls')
elif os.name == 'posix':
    os.system('clear')
banner = """
░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░▒▓████████▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓██████▓▒░ ░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░     
   ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓████████▓▒░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░  ░▒▓█▓▒░     
                                                                                        """
print(banner)
bot.infinity_polling()