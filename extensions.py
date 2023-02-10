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
    message = "Неверное количество параметров.\nВведи команду еще раз."

class QuoteException(Exception):
    message = "Введена несущеcтвующая переводимая валюта.\nВведи команду еще раз."

class BaseCurrencyException(Exception):
    message = "Введена несущеcтвующая валюта для перевода.\nВведи команду еще раз."

class EqualValues(Exception):
    message = "Одинаковые валюты для конвертации.\nВведи команду еще раз."
