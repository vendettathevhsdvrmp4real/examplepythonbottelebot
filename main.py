import telebot
from config import token

import random
import logging
import sys
import time
import os

from telebot import types 
from telebot.types import ReactionTypeEmoji 
from telebot import formatting
from logic import Pokemon

bot = telebot.TeleBot(token)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am TestBot.
just a test:) use command /help
""")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """\
the commands: /poll, /username
and the fun: /altf4, /system32, /downloadavatar, /avatar
""")
    
@bot.message_handler(commands=['altf4'])
def send_altf4message(message):
    bot.reply_to(message, """\
Bot:*alt+f4*.
Bot:oh nevermind im a bot and im never making alt+f4
""")

@bot.message_handler(commands=['system32'])
def send_jokesystem32meme(message):
    photo = open('badpiggies.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, caption='nuh uh')

@bot.message_handler(commands=["poll"])
def create_poll(message):
    bot.send_message(message.chat.id, "Programming Test")
    answer_options = ["Python", "Java", "C#", "C++"]

    bot.send_poll(
        chat_id=message.chat.id,
        question="what the code this? using System.IO; using System.Windows.Forms;",
        options=answer_options,
        type="quiz",
        correct_option_id=2,
        is_anonymous=False,
    )


@bot.poll_answer_handler()
def handle_poll(poll):
    user_id = poll.user.id
    selected_option = poll.option_ids[0]  # Get the user's answer
    correct_option = 2  # The correct answer (C#)

    if selected_option == correct_option:
        bot.send_message(user_id, "✅")
    else:
        bot.send_message(user_id, "❌")
    
# Send a reactions to all messages with content_type 'text' (content_types defaults to ['text'])

@bot.message_handler(commands=["downloaderavatar"])
def downloaderavatar(message):
    bot.send_message(message.chat.id, "Download avatar feature coming soon!!!")

MAX_ATTEMPTS = 5
user_data = {}

@bot.message_handler(commands=['game'])
def start_game(message):
    chat_id = message.chat.id
    user_data[chat_id] = {
        'number': random.randint(1, 100),
        'attempts': 0
    }
    bot.send_message(chat_id, f"Я загадал число от 1 до 100. У вас {MAX_ATTEMPTS} попыток. Попробуйте угадать!")

@bot.message_handler(func=lambda message: message.chat.id in user_data)
def guess_number(message):
    chat_id = message.chat.id
    try:
        guess = int(message.text)
        user_info = user_data[chat_id]
        number = user_info['number']
        user_info['attempts'] += 1

        if guess < number:
            bot.send_message(chat_id, "Загаданное число больше!")
        elif guess > number:
            bot.send_message(chat_id, "Загаданное число меньше!")
        else:
            bot.send_message(chat_id, f"Поздравляю! Вы угадали число за {user_info['attempts']} попыток! Начнем сначала? Напишите /start")
            del user_data[chat_id]
            return

        if user_info['attempts'] >= MAX_ATTEMPTS:
            bot.send_message(chat_id, f"Игра окончена! Вы не угадали число {number}. Попробуйте снова: /start")
            del user_data[chat_id]
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите число.")

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        bot.send_voice(message.chat.id, pokemon.show_audio())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


bot.infinity_polling()
