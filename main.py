import telebot
from currency_converter import CurrencyConverter

from settings import TELEGRAM_TOKEN

conversion = CurrencyConverter

converter_bot = telebot.TeleBot(TELEGRAM_TOKEN)


@converter_bot.message_handler(commands=["start"])
def start(message):
    """ Функция приветствия пользователя """
    hello = f"Привет, {message.from_user.first_name}рад тебя видеть!👋"
    converter_bot.send_message(message.chat.id, hello)


converter_bot.polling(none_stop=True)
