from flask import Flask, request
from payment_handler import handle_ipn

app = Flask(__name__)

@app.route("/")
def home():
    return "BlockScan AI Backend is running", 200


@app.route("/ipn", methods=["POST"])
def ipn():
    """
    NOWPayments sends payment notifications (webhooks) to this endpoint.
    """
    data = request.json

    if not data:
        return "No data received", 400

    if handle_ipn(data):
        return "OK", 200

    return "FAILED", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
