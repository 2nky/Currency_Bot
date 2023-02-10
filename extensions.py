import requests
import json

from config import API_TOKEN
from constants import keys


class GetPrice:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        if quote == base:
            raise EqualValues

        if quote not in keys:
            raise QuoteException

        if base not in keys:
            raise BaseCurrencyException

        quote_ticker, base_ticker = keys[quote], keys[base]
        r = requests.get(
            f'http://api.freecurrencyapi.com/v1/latest?apikey={API_TOKEN}&currencies={base_ticker}&base_currency={quote_ticker}'
        )
        total_base = json.loads(r.content)["data"][keys[base]]
        return total_base * amount



class ConvertionException(Exception):
    def __str__(self):
        return "Неверное количествоа параметров.\nВведи команду еще раз."

class QuoteException(Exception):
    def __str__(self):
        return "Введена несущетсвующая переводимая валюта.\nВведи команду еще раз."

class BaseCurrencyException(Exception):
    def __str__(self):
        return "Введена несущетсвующая валюта для перевода.\n Введи команду еще раз."

class EqualValues(Exception):
    def __str__(self):
        return "Одинаковые валюты для конвртации.\n Введи команду еще раз."


