import requests
from config import EXCHANGE_RATE_API_KEY

EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6"

def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount

    url = f"{EXCHANGE_RATE_URL}/{EXCHANGE_RATE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch exchange rates")

    data = response.json()
    return data['conversion_result']
