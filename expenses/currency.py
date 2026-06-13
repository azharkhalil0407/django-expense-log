import requests
import os
from decimal import Decimal

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USD")
EXCHANGE_RATE_API_URL = os.getenv("EXCHANGE_RATE_API_URL", "https://api.exchangerate.host")


def get_exchange_rate(from_currency, to_currency):
    """Fetch exchange rate from one currency to another."""
    if from_currency == to_currency:
        return Decimal("1.00")
    
    try:
        url = f"{EXCHANGE_RATE_API_URL}/convert"
        params = {"from": from_currency, "to": to_currency, "amount": 1}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return Decimal(str(data.get("result", 1)))
    except Exception as e:
        print(f"Exchange rate fetch failed: {e}")
        return Decimal("1.00")


def convert_amount(amount, from_currency, to_currency):
    """Convert amount from one currency to another."""
    rate = get_exchange_rate(from_currency, to_currency)
    return Decimal(str(amount)) * rate