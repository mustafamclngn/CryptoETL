import pandas as pd
from sqlalchemy.orm import Session
from db.models import CryptoPrice, get_engine

def load(df: pd.DataFrame):
    engine = get_engine()
    records = df.to_dict(orient="records")

    with Session(engine) as session:
        for row in records:
            session.add(CryptoPrice(**row))
        session.commit()

    print(f"[LOAD] Inserted {len(records)} rows into PostgreSQL.")