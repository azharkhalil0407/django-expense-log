import os
import requests
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")
BASE_CURRENCY = os.getenv("BASE_CURRENCY", "USD")


def send_telegram_alert(message):
    """Send alert message to Telegram."""
    if not BOT_TOKEN or not BOT_CHAT_ID:
        print("Bot credentials not configured")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": BOT_CHAT_ID, "text": message}
        response = requests.post(url, data=data, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram alert failed: {e}")
        return False


def check_budget_alert(expense):
    """Check if expense pushes category over monthly limit and send alert."""
    category = expense.category
    
    if not category.monthly_limit:
        return
    
    # Get current month total for this category
    now = timezone.now()
    month_start = now.replace(day=1)
    
    month_total = Decimal("0.00")
    for exp in category.expenses.filter(
        user=expense.user,
        date__year=now.year,
        date__month=now.month
    ):
        month_total += exp.amount
    
    # Check if over limit
    if month_total > category.monthly_limit:
        message = (
            f"Budget alert: \"{category.name}\" is over its monthly limit.\n"
            f"Spent {month_total} / {category.monthly_limit} {BASE_CURRENCY} for {now.strftime('%B %Y')}."
        )
        send_telegram_alert(message)