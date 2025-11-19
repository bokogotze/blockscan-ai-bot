import os
import requests
from database import set_premium

API_KEY = os.getenv("NOWPAYMENTS_API_KEY")
IPN_SECRET = os.getenv("NOWPAYMENTS_IPN_SECRET")

NOWPAYMENTS_INVOICE_URL = "https://api.nowpayments.io/v1/invoice"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def create_invoice(user_id, currency="usdt", amount=49):
    """
    Create a NOWPayments invoice for a user's premium subscription.
    """
    data = {
        "price_amount": amount,
        "price_currency": "usd",
        "pay_currency": currency,
        "order_id": str(user_id),
        "order_description": f"BlockScan AI Premium for user {user_id}",
        "ipn_callback_url": "https://YOUR-RENDER-URL.onrender.com/ipn"
    }

    response = requests.post(NOWPAYMENTS_INVOICE_URL, json=data, headers=headers)
    r = response.json()

    return r.get("invoice_url"), r.get("id")


def handle_ipn(ipn_data):
    """
    Handle NOWPayments webhook notifications.
    """
    # Verify the IPN secret
    received_secret = ipn_data.get("ipn_secret")
    if received_secret != IPN_SECRET:
        return False

    status = ipn_data.get("payment_status")
    
    if status == "finished":
        user_id = int(ipn_data.get("order_id"))
        set_premium(user_id, 30)  # 30 days premium
        return True

    return False
