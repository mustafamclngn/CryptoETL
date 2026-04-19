import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def extract(vs_currency="usd", top_n=10) -> list[dict]:
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": top_n,
        "page": 1,
        "sparkline": False,
    }
    response = requests.get(COINGECKO_URL, params=params, timeout=10)
    response.raise_for_status()
    print(f"[EXTRACT] Fetched {len(response.json())} coins.")
    return response.json()