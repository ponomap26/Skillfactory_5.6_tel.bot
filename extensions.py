import requests
import json
from config import keys


class APIException(Exception):
    pass


class MoneyConvertor:
    @staticmethod
    def convert(quote, base, amount):
        keys[quote], keys[base] = keys[quote], keys[base]
        quote_ticker, base_ticker = keys[quote], keys[base]
        if quote == base:
            raise APIException(f'Вы ввели одинаковые валюты {base}.')
        try:
            quote_ticker == keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')
        try:
            base_ticker == keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total = json.loads(r.content)[keys[base]] * amount
        return total
