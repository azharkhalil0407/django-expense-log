import requests
import os
from decimal import Decimal

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USD")
EXCHANGE_RATE_API_URL = os.getenv("EXCHANGE_RATE_API_URL", "https://open.er-api.com/v6/latest")


def get_exchange_rate(from_currency, to_currency):
    """Fetch exchange rate from one currency to another."""
    if from_currency == to_currency:
        return Decimal("1.00")
    
    try:
        url = f"{EXCHANGE_RATE_API_URL}/{from_currency}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("result") == "success":
            rates = data.get("rates", {})
            rate = rates.get(to_currency, 1)
            return Decimal(str(rate))
        else:
            print(f"API error: {data.get('error', 'Unknown error')}")
            return Decimal("1.00")
    except Exception as e:
        print(f"Exchange rate fetch failed: {e}")
        return Decimal("1.00")


def convert_amount(amount, from_currency, to_currency):
    """Convert amount from one currency to another."""
    rate = get_exchange_rate(from_currency, to_currency)
    return Decimal(str(amount)) * rate


def convert_amount_with_rate(amount, from_currency, to_currency):
    """Convert amount and return both converted amount and rate used."""
    rate = get_exchange_rate(from_currency, to_currency)
    converted = Decimal(str(amount)) * rate
    return converted, rate