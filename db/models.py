from sqlalchemy import create_engine, Column, String, Float, BigInteger, DateTime
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id               = Column(BigInteger, primary_key=True, autoincrement=True)
    coin_id          = Column(String, nullable=False)
    symbol           = Column(String)
    name             = Column(String)
    current_price    = Column(Float)
    market_cap       = Column(Float)
    total_volume     = Column(Float)
    price_change_24h = Column(Float)
    fetched_at       = Column(DateTime, nullable=False)

def get_engine():
    return create_engine(os.getenv("DATABASE_URL"))

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Tables created successfully.")