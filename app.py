import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    text = f'Я бот-конвертер! \n' \
           f'Список доступных для конвертирования валют /values \n' \
           f'Формат ввода валют -> доллар рубль 100'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException(f'Неверное количество параметров \n'
                               f'Формат ввода валют -> доллар рубль 100')

        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()
        amount = float(amount)
        total_base = Converter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f' {amount} {keys[quote]} = {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)



bot.polling()
