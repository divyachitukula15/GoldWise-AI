from goldwise.data.upstox import fetch_combined_history
from goldwise.database import save_rates

if __name__ == "__main__":
    history = fetch_combined_history()
    save_rates(history)
    print(f"Saved market rates for {len(history)} dates.")
