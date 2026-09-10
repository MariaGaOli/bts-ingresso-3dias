import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_message(text: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID não configurados.")
    response = requests.post(
        API,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "disable_web_page_preview": False},
        timeout=30,
    )
    response.raise_for_status()

def test_message() -> None:
    send_message("✅ Monitor BTS 3 dias — teste do Telegram funcionando.")
