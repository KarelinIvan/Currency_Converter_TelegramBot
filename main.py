import telebot

from settings import TELEGRAM_TOKEN

converter_bot = telebot.TeleBot(TELEGRAM_TOKEN)

@converter_bot.message_handler(commands=["start"])
def start(message):
    """ Функция приветствия пользователя """
    hello = f"Привет, {message.from_user.first_name}рад тебя видеть!👋"
    converter_bot.send_message(message.chat.id, hello)
