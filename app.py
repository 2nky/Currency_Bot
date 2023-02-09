import telebot

from config import TOKEN
from constants import keys
from extensions import ConvertionException, GetPrice, EqualValues, QuoteException, BaseCurrencyException, AmountExeption


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "Чтобы конвертировать валюту введите:\n <название переводимой валюты>\
    <название валюты, в которую переводите> \
    <количество валюты> \n <Чтобу увидеть список доступных валют введите: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(messege: telebot.types.Message):
    text = "<Достпные валюты>:"
    for key in keys.keys():
        text = "\n" .join((text, key, ))
    bot.reply_to(messege, text)

@bot.message_handler(content_types =["text", ])
def convert(messege: telebot.types.Message):
    values = messege.text.split(" ")
    quote, base, amount = values

    try:
        if len(values) != 3:
            raise ConvertionException

        result = GetPrice.get_price(quote, base, float(amount))
        text = f'{amount} {quote} в {base} - {result}'
        bot.send_message(messege.chat.id, text)

    except EqualValues:
        bot.reply_to(messege, "Одинаковые валюты для конвртации.\n Введи команду еще раз.")

    except QuoteException:
        bot.reply_to(messege, "Введена несущетсвующая переводимая валюта.\nВведи команду еще раз.")

    except BaseCurrencyException:
        bot.reply_to(messege, "Введена несущетсвующая валюта для перевода.\n Введи команду еще раз.")

    except ConvertionException:
        bot.reply_to(messege, "Неверное количествоа параметров.\nВведи команду еще раз.")

    except AmountExeption:
        bot.reply_to(messege, "Количесто валюты должно быть числом.\n Введи команду еще раз.")

    except:
        bot.reply_to(messege, "Ошибка сервера.\nВведи команду еще раз.")
        raise


bot.polling()
