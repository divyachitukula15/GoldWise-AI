import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from goldwise.services.change_detection import detect_changes, update_snapshot
from goldwise.data.upstox import fetch_combined_history
from goldwise.database import save_rates
from goldwise.notifications.telegram import send_telegram_message

load_dotenv()

def build_change_report(latest, changes):
    lines = ["GoldWise AI - Kamareddy Market Update", "", "Latest rates (per 10 grams):"]
    for metal, data in latest.items():
        lines.append(f"- {metal}: Rs. {float(data['rate']):,.2f} (Date: {data['date']})")

    lines.extend(["", "Changes since previous report:"])
    for item in changes:
        if item["old_rate"] is None:
            lines.append(f"- {item['metal']}: baseline not available; current Rs. {item['new_rate']:,.2f}")
        else:
            lines.append(
                f"- {item['metal']}: Rs. {item['old_rate']:,.2f} -> "
                f"Rs. {item['new_rate']:,.2f} "
                f"({item['difference']:+,.2f}, {item['percentage']:+.2f}%)"
            )

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY in .env")

    llm = ChatOpenAI(
        model="openrouter/free",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0.2,
    )
    prompt = f"""
    Rewrite this data as a short Telegram update in Telugu-English using English letters only.
    Keep all figures, dates, and percentages exactly unchanged. Do not add facts or predictions.
    DATA:
    {chr(10).join(lines)}
    """
    return llm.invoke(prompt).content

if __name__ == "__main__":
    # Refresh market data before comparing it with the previous report snapshot.
    save_rates(fetch_combined_history())
    latest, changes = detect_changes()

    if latest is None:
        print("No market data available.")
    elif changes is None:
        print("No previous snapshot found. Run the daily report once to establish baseline.")
    elif not changes:
        print("No rate changes. Telegram notification skipped.")
    else:
        report = build_change_report(latest, changes)
        send_telegram_message(report)
        update_snapshot(latest)
        print("Changed-rate Telegram report sent; snapshot updated.")
