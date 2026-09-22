import os
from dotenv import load_dotenv

load_dotenv()

EVENTS = {
    "28/10/2026": "https://buyticketbrasil.com/event/bts-2026worldtourarirang/session/ced30381-0cc4-4779-9c6b-ba05f44d086e",
    "30/10/2026": "https://buyticketbrasil.com/event/bts-2026worldtourarirang/session/e4ac9384-ccd7-4f29-82b8-7ba8677bc2ed",
    "31/10/2026": "https://buyticketbrasil.com/event/bts-2026worldtourarirang/session/7dbb3a2b-985d-4bf2-9d36-df893169e098",
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

PRICE_LIMIT = float(os.getenv("PRICE_LIMIT", "1000"))
MIN_DROP_REAIS = float(os.getenv("MIN_DROP_REAIS", "500"))
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "300"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
STATE_FILE = "state.json"
