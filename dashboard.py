import streamlit as st
import pandas as pd
from sqlalchemy import text
from db.models import get_engine

st.set_page_config(page_title="Crypto Pipeline", layout="wide")
st.title("CryptoETL")
st.caption("An automated cryptocurrency pipeline that extracts data from CoinGecko API")

engine = get_engine()

# ── helpers ────────────────────────────────────────────────────────────────

def get_latest_prices():
    query = text("""
        SELECT DISTINCT ON (coin_id)
            coin_id, symbol, name, current_price,
            price_change_24h, market_cap, fetched_at, image_url
        FROM crypto_prices
        ORDER BY coin_id, fetched_at DESC
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

df = get_latest_prices()

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

st.markdown("""
    <style>
    [data-testid="stMetric"] {
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 10px;
        padding: 16px;
    }
    .coin-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(128, 128, 128, 0.3);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 8px;
    }
    .coin-card-left { display: flex; flex-direction: column; gap: 4px; }
    .coin-card-label { font-size: 14px; color: gray; }
    .coin-card-value { font-size: 24px; font-weight: bold; }
    .coin-card-delta-pos { font-size: 14px; color: #09ab3b; }
    .coin-card-delta-neg { font-size: 14px; color: #ff2b2b; }
    .coin-card-img { width: 48px; height: 48px; object-fit: contain; }
    </style>
""", unsafe_allow_html=True)

cols = st.columns(5)
for i, row in df.head(5).iterrows():
    change = row['price_change_24h']
    delta_class = "coin-card-delta-pos" if change >= 0 else "coin-card-delta-neg"
    delta_sign = "▲" if change >= 0 else "▼"
    image_tag = f'<img class="coin-card-img" src="{row["image_url"]}">' if pd.notna(row.get("image_url")) and row["image_url"] else ""

    with cols[i % 5]:
        st.markdown(f"""
            <div class="coin-card">
                <div class="coin-card-left">
                    <div class="coin-card-label">{row['name']} ({row['symbol'].upper()})</div>
                    <div class="coin-card-value">${row['current_price']:,.2f}</div>
                    <div class="{delta_class}">{delta_sign} {abs(change):.2f}%</div>
                </div>
                {image_tag}
            </div>
        """, unsafe_allow_html=True)

# ── price table ────────────────────────────────────────────

st.subheader("Price Table")
st.caption("Price records are extracted every 10 minutes")

table = df[["name", "symbol", "current_price", "price_change_24h", "market_cap", "fetched_at"]].copy()
table.columns = ["Coin", "Symbol", "Price (USD)", "24h Change %", "Market Cap", "Last Updated"]
table["Symbol"] = table["Symbol"].str.upper()
table["Price (USD)"] = table["Price (USD)"].apply(lambda x: f"${x:,.4f}")
table["Market Cap"] = table["Market Cap"].apply(lambda x: f"${x:,.0f}")
table["24h Change %"] = table["24h Change %"].apply(
    lambda x: f"🟢 +{x:.2f}%" if x >= 0 else f"🔴 {x:.2f}%"
)
table = table.reset_index(drop=True)
st.dataframe(table, width='stretch', hide_index=True)