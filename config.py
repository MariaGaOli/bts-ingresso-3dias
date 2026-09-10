import os
from dotenv import load_dotenv

load_dotenv()

EVENTS = {
    "28/10/2026": "https://buyticketbrasil.com/evento/bts%E2%80%932026worldtourarirang?data=1793242799000&evento_local=1775752182066x607042691407020000&cidade=S%C3%A3o+Paulo",
    "30/10/2026": "https://buyticketbrasil.com/evento/bts%E2%80%932026worldtourarirang?data=1793415599000&evento_local=1775752182066x607042691407020000&cidade=S%C3%A3o+Paulo",
    "31/10/2026": "https://buyticketbrasil.com/evento/bts%E2%80%932026worldtourarirang?data=1793501999000&evento_local=1775752182066x607042691407020000&cidade=S%C3%A3o+Paulo",
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

PRICE_LIMIT = float(os.getenv("PRICE_LIMIT", "1000"))
MIN_DROP_REAIS = float(os.getenv("MIN_DROP_REAIS", "500"))
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "300"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
STATE_FILE = "state.json"
