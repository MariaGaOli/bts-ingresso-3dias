import re
from dataclasses import dataclass, asdict
from typing import Optional
from playwright.sync_api import sync_playwright
from config import EVENTS, HEADLESS

PRICE_RE = re.compile(r"R\$\s*([\d.]+(?:,\d{2})?)", re.I)

@dataclass
class Ticket:
    date: str
    category: str
    ticket_type: str
    price: float
    raw_price: str
    url: str
    text: Optional[str] = None

    def to_dict(self):
        return asdict(self)

def parse_price(value: str) -> Optional[float]:
    match = PRICE_RE.search(value or "")
    if not match:
        return None
    try:
        return float(match.group(1).replace(".", "").replace(",", "."))
    except ValueError:
        return None

def money(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def visible_price_buttons(page):
    items = []
    for button in page.locator("button").all():
        try:
            if not button.is_visible():
                continue
            text = re.sub(r"\s+", " ", button.inner_text()).strip()
            if parse_price(text) is not None:
                items.append(text)
        except Exception:
            pass
    return items

def open_menu(page, name: str):
    button = page.get_by_role("button", name=name, exact=True)
    button.wait_for(state="visible", timeout=15000)
    button.click()
    page.wait_for_timeout(700)

def scrape_event(page, date: str, url: str) -> list[Ticket]:
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3500)
    results = []

    open_menu(page, "Tipo de ingresso")
    sector_items = visible_price_buttons(page)
    sectors = []
    for item in sector_items:
        pos = item.find("R$")
        name = item[:pos].strip() if pos >= 0 else ""
        if name and name not in sectors:
            sectors.append(name)

    for sector in sectors:
        if "camarote" in sector.lower():
            continue  
        try:
            option = page.get_by_text(sector, exact=True)
            if option.count() == 0:
                continue
            option.first.click()
            page.wait_for_timeout(900)

            open_menu(page, "Categoria")
            category_items = visible_price_buttons(page)

            for item in category_items:
                pos = item.find("R$")
                if pos < 0:
                    continue
                category = item[:pos].strip()
                price = parse_price(item)
                if not category or category.lower() == "categoria" or price is None or price <= 0:
                    continue

                results.append(Ticket(
                    date=date,
                    category=sector,
                    ticket_type=category,
                    price=price,
                    raw_price=money(price),
                    url=url,
                    text=f"{sector} • {category} • {money(price)}",
                ))

            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1800)
            open_menu(page, "Tipo de ingresso")

        except Exception as exc:
            print(f"[{date}] Falha ao ler setor {sector}: {type(exc).__name__}: {exc}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(1800)
                open_menu(page, "Tipo de ingresso")
            except Exception:
                break

    return results

def scrape() -> list[Ticket]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, locale="pt-BR")
        try:
            all_tickets = []
            for date, url in EVENTS.items():
                print(f"\n===== {date} =====")
                tickets = scrape_event(page, date, url)
                all_tickets.extend(tickets)
                print(f"[{date}] {len(tickets)} combinações encontradas.")
            return all_tickets
        finally:
            browser.close()
