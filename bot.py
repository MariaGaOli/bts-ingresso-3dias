import argparse
import time
from datetime import datetime
from config import CHECK_INTERVAL_SECONDS, MIN_DROP_REAIS, PRICE_LIMIT
from scraper import scrape, Ticket
from state import load_state, save_state
from telegram import send_message, test_message

def brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def ticket_key(ticket: Ticket) -> str:
    return f"{ticket.date}|{ticket.category}|{ticket.ticket_type}"

def drop_message(previous: float, ticket: Ticket) -> str:
    drop = previous - ticket.price
    percent = (drop / previous * 100) if previous else 0
    return (
        "📉 Queda de preço — BTS\n\n"
        f"📅 {ticket.date}\n"
        f"🎟 {ticket.category} • {ticket.ticket_type}\n\n"
        f"Antes: {brl(previous)}\n"
        f"Agora: {brl(ticket.price)}\n"
        f"↓ {brl(drop)} ({percent:.1f}%)\n\n"
        f"🔗 {ticket.url}"
    )

def target_message(ticket: Ticket) -> str:
    return (
        "🚨🚨 INGRESSO ATÉ R$ 1.000! 🚨🚨\n\n"
        f"📅 {ticket.date}\n"
        f"🎟 {ticket.category} • {ticket.ticket_type}\n\n"
        f"💰 {brl(ticket.price)}\n\n"
        "🔥 ESSE VALOR ENTROU NO LIMITE!\n\n"
        f"🔗 {ticket.url}"
    )

def process_ticket(state: dict, ticket: Ticket):
    k = ticket_key(ticket)
    data = state["tickets"].get(k, {})
    previous = data.get("last_seen")
    target_alerted = data.get("target_alerted", False)

    if ticket.price <= PRICE_LIMIT and not target_alerted:
        send_message(target_message(ticket))
        data["target_alerted"] = True

    if previous is not None and previous - ticket.price >= MIN_DROP_REAIS:
        send_message(drop_message(previous, ticket))

    data["last_seen"] = ticket.price
    data["lowest"] = min(data.get("lowest", ticket.price), ticket.price)
    state["tickets"][k] = data

def process_once(state: dict):
    tickets = scrape()
    if not tickets:
        print("Nenhum ingresso encontrado.")
        return state

    for ticket in tickets:
        try:
            process_ticket(state, ticket)
        except Exception as exc:
            print(f"Erro em {ticket.date} / {ticket.category} / {ticket.ticket_type}: {type(exc).__name__}: {exc}")

    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {len(tickets)} combinações monitoradas.")
    save_state(state)
    return state

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-telegram", action="store_true")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    if args.test_telegram:
        test_message()
        print("Mensagem de teste enviada.")
        return

    state = load_state()
    while True:
        try:
            state = process_once(state)
        except Exception as exc:
            print(f"Erro na verificação: {type(exc).__name__}: {exc}")
        if args.once:
            break
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
