import telebot
from currency_converter import CurrencyConverter
from telebot import types

from settings import TELEGRAM_TOKEN

conversion = CurrencyConverter()

converter_bot = telebot.TeleBot(TELEGRAM_TOKEN)

amount = 0


@converter_bot.message_handler(commands=["start"])
def start(message):
    """ Функция приветствия пользователя """
    hello = (f"Привет, {message.from_user.first_name}, рад тебя видеть!👋\n"
             f"Введите сумму для конвертации")
    converter_bot.send_message(message.chat.id, hello)
    converter_bot.register_next_step_handler(message, conversion_amount)


def conversion_amount(message):
    """ Проверка корректного ввода и интерфейс """
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        info_message_2 = "Некорректный ввод, введите сумму!"
        converter_bot.send_message(message.chat.id, info_message_2)
        converter_bot.register_next_step_handler(message, conversion_amount)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("RUB/USD", callback_data="rub/usd")
        btn2 = types.InlineKeyboardButton("RUB/EUR", callback_data="rub/eur")
        btn3 = types.InlineKeyboardButton("Другая валютная пара", callback_data="else")
        markup.add(btn1, btn2, btn3)
        info_message = "Выберите валютную пару или введите свою"
        converter_bot.send_message(message.chat.id, info_message, reply_markup=markup)
    else:
        info_message_3 = "Некорректный ввод, сумма должна быть больше ноля!"
        converter_bot.send_message(message.chat.id, info_message_3)
        converter_bot.register_next_step_handler(message, conversion_amount)


@converter_bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """ Функция для конвертации валют """
    values = call.data.upper().split("/")
    result = conversion.convert(amount, values[0], values[1])
    info_message_3 = (f"В настоящее время курс пары {values[0]} к {values[1]},\n"
                      f"{amount} {values[0]} = {round(result, 2)} {values[1]}\n"
                      f"Введите следующую сумму для конвертации")
    converter_bot.send_message(call.message.chat.id, info_message_3)
    converter_bot.register_next_step_handler(call.message, conversion_amount)


converter_bot.polling(none_stop=True)
