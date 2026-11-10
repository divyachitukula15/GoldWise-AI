import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}
GOLD_URL = "https://upstox.com/gold-rates/gold-rates-in-kamareddy/"
SILVER_URL = "https://upstox.com/silver-rates/silver-rates-in-kamareddy/"

def fetch_page(url: str):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def _extract_price(text: str):
    match = re.search(r"₹\s*([\d,]+\.\d{2})", text)
    return float(match.group(1).replace(",", "")) if match else None

def extract_gold_history(soup):
    history = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue
        header = rows[0].get_text(" ", strip=True)
        if "Date" not in header or "24K Gold" not in header:
            continue

        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) < 3:
                continue
            parsed_date = datetime.strptime(
                cells[0].get_text(strip=True), "%d %b %Y"
            ).strftime("%Y-%m-%d")
            history.append({
                "date": parsed_date,
                "24K": _extract_price(cells[1].get_text(" ", strip=True)),
                "22K": _extract_price(cells[2].get_text(" ", strip=True)),
                "silver": None,
            })
        break

    if not history:
        raise ValueError("Gold historical data not found on Upstox page")
    return history

def extract_silver_history(soup, year=None):
    history = []
    year = year or datetime.now().year

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue
        header = rows[0].get_text(" ", strip=True)
        if "Date" not in header or "Silver Rates" not in header:
            continue

        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            price = _extract_price(cells[1].get_text(" ", strip=True))
            if price is None:
                continue

            date_text = cells[0].get_text(strip=True)
            try:
                parsed = datetime.strptime(date_text, "%d %b %Y")
            except ValueError:
                parsed = datetime.strptime(f"{date_text} {year}", "%b %d %Y")

            history.append({
                "date": parsed.strftime("%Y-%m-%d"),
                "24K": None,
                "22K": None,
                # Upstox silver page displays per 100g; normalize to per 10g.
                "silver": price / 10,
            })
        break

    if not history:
        raise ValueError("Silver historical data not found on Upstox page")
    return history

def fetch_combined_history():
    gold_soup = fetch_page(GOLD_URL)
    silver_soup = fetch_page(SILVER_URL)

    gold_history = extract_gold_history(gold_soup)
    reference_year = datetime.strptime(gold_history[0]["date"], "%Y-%m-%d").year
    silver_history = extract_silver_history(silver_soup, year=reference_year)

    combined = {}
    for item in gold_history + silver_history:
        day = item["date"]
        if day not in combined:
            combined[day] = {
                "date": day, "24K": None, "22K": None, "silver": None
            }
        for metal in ("24K", "22K", "silver"):
            if item.get(metal) is not None:
                combined[day][metal] = item[metal]

    return sorted(combined.values(), key=lambda item: item["date"], reverse=True)
