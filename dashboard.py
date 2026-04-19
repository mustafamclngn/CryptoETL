import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.models import get_engine

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("CryptoETL")
st.caption("Data is being extracted every 10 minutes")

engine = get_engine()

# ── helpers ────────────────────────────────────────────────────────────────

def get_latest_prices():
    query = text("""
        SELECT DISTINCT ON (coin_id)
            coin_id, symbol, name, current_price,
            price_change_24h, market_cap, fetched_at
        FROM crypto_prices
        ORDER BY coin_id, fetched_at DESC
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def get_price_history(coin_id: str):
    query = text("""
        SELECT fetched_at, current_price
        FROM crypto_prices
        WHERE coin_id = :coin_id
        ORDER BY fetched_at ASC
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params={"coin_id": coin_id})

# ── data ───────────────────────────────────────────────────────────────────

df = get_latest_prices()

# ── top coins cards ────────────────────────────────────────────────

st.subheader("Top Coins")
st.caption("24-hour change for each of the coins are shown")

cols = st.columns(5)
for i, row in df.head(5).iterrows():
    delta = f"{row['price_change_24h']:+.2f}%"
    cols[i % 5].metric(
        label=f"{row['name']} ({row['symbol'].upper()})",
        value=f"${row['current_price']:,.2f}",
        delta=delta
    )

st.divider()

# ── price table ────────────────────────────────────────────

st.subheader("Price Table")
st.caption("Latest recorded price for all tracked coins.")

table = df[["name", "symbol", "current_price", "price_change_24h", "market_cap", "fetched_at"]].copy()
table.columns = ["Coin", "Symbol", "Price (USD)", "24h Change %", "Market Cap", "Last Updated"]
table["Symbol"] = table["Symbol"].str.upper()
table["Price (USD)"] = table["Price (USD)"].apply(lambda x: f"${x:,.4f}")
table["Market Cap"] = table["Market Cap"].apply(lambda x: f"${x:,.0f}")
table["24h Change %"] = table["24h Change %"].apply(
    lambda x: f"🟢 +{x:.2f}%" if x >= 0 else f"🔴 {x:.2f}%"
)
table = table.reset_index(drop=True)
st.dataframe(table, use_container_width=True, hide_index=True)

st.divider()

# ── 24 hours price change ───────────────────────────────────────

st.subheader("24 hour Price Change")
st.caption("Which coins gained or lost the most in the last 24 hours.")

change_df = df[["name", "price_change_24h"]].sort_values("price_change_24h", ascending=False)
st.bar_chart(change_df.set_index("name")["price_change_24h"], use_container_width=True)