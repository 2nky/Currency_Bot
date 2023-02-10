import telebot

from config import TOKEN
from constants import keys
from extensions import ConvertionException, GetPrice, EqualValues, QuoteException, BaseCurrencyException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "Чтобы конвертировать валюту введи:\n<название конвертируемой валюты>\n" \
        "<название валюты, в которую конвертируем> \n" \
        "<количество валюты> \n\n Чтобы увидеть список доступных валют введи:\n/values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def values(messege: telebot.types.Message):
    text = "<Доступные валюты>:"
    for key in keys.keys():
        text = "\n" .join((text, key, ))
    bot.reply_to(messege, text)

@bot.message_handler(content_types =["text", ])
def convert(messege: telebot.types.Message):
    values = messege.text.split(" ")

    try:
        if len(values) != 3:
            raise ConvertionException

        quote, base, amount = values

        result = GetPrice.get_price(quote, base, float(amount))
        text = f'{amount} {quote} в {base} - {result:.2f}'
        bot.send_message(messege.chat.id, text)

    except EqualValues:
        bot.reply_to(messege, "Одинаковые валюты для конвертации.\nВведи команду еще раз.")

    except QuoteException:
        bot.reply_to(messege, "Введена несуществующая конвертируемая валюта.\nВведи команду еще раз.")

    except BaseCurrencyException:
        bot.reply_to(messege, "Введена несуществующая валюта для конвертации.\nВведи команду еще раз.")

    except ConvertionException:
        bot.reply_to(messege, "Неверное количество параметров.\nВведи команду еще раз.")

    except ValueError:
        bot.reply_to(messege,"Ошибка ввода количесвта валюты.\nВведи команду еще раз.")

    except:
        bot.reply_to(messege, "Ошибка сервера.\nВведи команду еще раз.")
        raise


bot.polling()
