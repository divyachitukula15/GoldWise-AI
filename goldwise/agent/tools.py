from langchain_core.tools import tool
from goldwise.database import METALS, get_latest_rates, get_price_history

@tool
def latest_market_rates() -> list:
    """Get the latest available Kamareddy gold and silver rates per 10 grams."""
    rates = get_latest_rates()
    return [
        {"metal": metal, "date": str(data["date"]), "rate_per_10g": float(data["rate"])}
        for metal, data in rates.items()
    ]

@tool
def market_price_history(metal: str) -> list:
    """Get up to 15 latest available rates for 24K, 22K, or silver."""
    if metal not in METALS:
        return [{"error": f"metal must be one of {METALS}"}]
    return [
        {"date": str(day), "rate_per_10g": float(rate)}
        for day, rate in get_price_history(metal, 15)
    ]

tools = [latest_market_rates, market_price_history]
