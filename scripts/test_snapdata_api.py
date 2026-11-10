import requests

BASE_URL = "https://snapdata.dev/api/v1"
ENDPOINTS = {
    "Gold": f"{BASE_URL}/gold/in/series/30d.json",
    "Silver": f"{BASE_URL}/silver/in/series/30d.json",
}

if __name__ == "__main__":
    for name, url in ENDPOINTS.items():
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        print(f"\\n--- {name} ---")
        print("Generated at:", data.get("generated_at"))
        for item in data.get("observations", []):
            print(item.get("date"), item.get("instrument"), item.get("value"))
