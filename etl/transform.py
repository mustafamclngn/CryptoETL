import pandas as pd
from datetime import datetime, timezone

COLUMNS = [
    "id", "symbol", "name",
    "current_price", "market_cap",
    "total_volume", "price_change_percentage_24h"
]

def transform(raw: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(raw)[COLUMNS]

    df = df.rename(columns={
        "id": "coin_id",
        "price_change_percentage_24h": "price_change_24h"
    })

    # convert to numeric, error handling
    df["current_price"]    = pd.to_numeric(df["current_price"],    errors="coerce")
    df["market_cap"]       = pd.to_numeric(df["market_cap"],       errors="coerce")
    df["total_volume"]     = pd.to_numeric(df["total_volume"],     errors="coerce")
    df["price_change_24h"] = pd.to_numeric(df["price_change_24h"], errors="coerce")

    # timestamp
    df["fetched_at"] = datetime.now(timezone.utc)

    print(f"[TRANSFORM] Cleaned {len(df)} rows.")
    return df