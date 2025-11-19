import requests

def fetch_json(url):
    """
    Simple GET request returning JSON data.
    """
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except:
        return {"error": "Failed to fetch data"}

def chunk_text(text, size=3800):
    """
    Splits long AI responses into smaller chunks so Telegram can send them.
    """
    return [text[i:i+size] for i in range(0, len(text), size)]
