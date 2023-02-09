import json
import requests
import telebot

TOKEN = "6027550278:AAEDIJr4skazdPv0yinQ6rMws0SVJl4psUc"

bot = telebot.TeleBot(TOKEN)

keys = {
    "евро": "EUR",
    "доллар": "USD",
    "йена": "JPY"
}
class GetPrice:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        if quote == base:
            raise EqualValues

        if quote not in keys:
            raise QuoteException

        if base not in keys:
            raise BaseException

        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(
            f'http://api.freecurrencyapi.com/v1/latest?apikey=ALTXe7rVH2CZrBfWaJPcZ4FeBuUK9X3r4Jo1YWsl&currencies={base_ticker}&base_currency={quote_ticker}'
        )
        total_base = json.loads(r.content)["data"][keys[base]]
        return total_base * amount



class ConvertionException(Exception):
    def __str__(self):
        return "Неверное количествоа параметров.\nВведи команду еще раз."

class QuoteException(Exception):
    def __str__(self):
        return "Введена несущетсвующая переводимая валюта.\nВведи команду еще раз."

class BaseException(Exception):
    def __str__(self):
        return "Введена несущетсвующая валюта для перевода.\n Введи команду еще раз."

class EqualValues(Exception):
    def __str__(self):
        return "Одинаковые валюты для конвртации.\n Введи команду еще раз."

class AmountExeption(Exception):
    def __str__(self):
        return "Количесто валюты должно быть числом.\n Введи команду еще раз."


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

    except BaseException:
        bot.reply_to(messege, "Введена несущетсвующая валюта для перевода.\n Введи команду еще раз.")

    except ConvertionException:
        bot.reply_to(messege, "Неверное количествоа параметров.\nВведи команду еще раз.")

    except AmountExeption:
        bot.reply_to(messege, "Количесто валюты должно быть числом.\n Введи команду еще раз.")

    except:
        bot.reply_to(messege, "Ошибка сервера.\nВведи команду еще раз.")
        raise


bot.polling()
