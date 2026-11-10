from langchain_core.messages import HumanMessage
from goldwise.agent.workflow import build_workflow
from goldwise.database import get_latest_rates, save_rates, update_snapshot
from goldwise.data.upstox import fetch_combined_history
from goldwise.notifications.telegram import send_telegram_message

if __name__ == "__main__":
    # Refresh database before generating the daily report.
    save_rates(fetch_combined_history())
    app = build_workflow()
    result = app.invoke({
        "messages": [HumanMessage(
            content="Give today's Kamareddy gold and silver market report with latest rates."
        )]
    })
    report = result["messages"][-1].content
    send_telegram_message(report)

    latest = get_latest_rates()
    if latest:
        update_snapshot(latest)
    print("Daily Telegram report sent; snapshot updated.")
