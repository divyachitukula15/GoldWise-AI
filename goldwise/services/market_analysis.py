from statistics import pstdev
from goldwise.database import METALS, get_price_history

def compare_latest_rates():
    results = {}
    for metal in METALS:
        rows = get_price_history(metal, limit=2)
        if len(rows) < 2:
            continue
        latest_date, latest = rows[0]
        previous_date, previous = rows[1]
        difference = float(latest - previous)
        results[metal] = {
            "latest_date": str(latest_date),
            "latest_rate": float(latest),
            "previous_date": str(previous_date),
            "previous_rate": float(previous),
            "difference": round(difference, 2),
            "percentage": round(difference / float(previous) * 100, 2),
            "status": "Increased" if difference > 0 else (
                "Decreased" if difference < 0 else "Unchanged"
            ),
        }
    return results

def analyze_trend(metal: str, limit: int = 15):
    rows = list(reversed(get_price_history(metal, limit)))
    if len(rows) < 2:
        return None

    dates = [str(row[0]) for row in rows]
    rates = [float(row[1]) for row in rows]
    changes = [
        (rates[i] - rates[i - 1]) / rates[i - 1] * 100
        for i in range(1, len(rates))
    ]
    high_index = rates.index(max(rates))
    low_index = rates.index(min(rates))

    return {
        "metal": metal,
        "records_count": len(rows),
        "start_date": dates[0],
        "end_date": dates[-1],
        "overall_difference": round(rates[-1] - rates[0], 2),
        "overall_percentage": round((rates[-1] - rates[0]) / rates[0] * 100, 2),
        "average_rate": round(sum(rates) / len(rates), 2),
        "highest_rate": rates[high_index],
        "highest_date": dates[high_index],
        "lowest_rate": rates[low_index],
        "lowest_date": dates[low_index],
        "volatility": round(pstdev(changes), 2) if len(changes) > 1 else 0.0,
    }
