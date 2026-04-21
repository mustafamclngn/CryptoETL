<div align="center">

# CryptoETL
### Crypto ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-Data%20Transform-150458?logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?logo=git&logoColor=white)

**A Python-based ETL pipeline that extracts cryptocurrency market data from the CoinGecko API, transforms it using pandas, loads it into PostgreSQL, and serves a live Streamlit dashboard for price monitoring and trend analysis.**

</div>

## SETUP & INSTALLATION

### 1. Clone the repository
```bash
git clone https://github.com/mustafamclngn/CryptoETL.git
cd CryptoETL
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database
```bash
createdb crypto_db
```

### 5. Configure environment variables
Create a `.env` file in the project root:

---

## HOW TO RUN

### Run the pipeline once
```bash
python pipeline.py
```

### Run the scheduler (fetches every 10 minutes)
```bash
python scheduler.py
```

### Launch the dashboard
Open a second terminal and run:
```bash
streamlit run dashboard.py
```
Then open your browser at `http://localhost:8501`

> **Tip:** Run the scheduler and dashboard at the same time in two separate
> terminals to see live data updates on the dashboard.

---
<div align="center">
  
## DASHBOARD
![Dashboard](screenshots/dashboard.png)

</div>
---

## DASHBOARD FEATURES
- **Top coins** — metric cards showing current price and 24h change
- **Price Table** — latest prices for all 10 tracked coins with color-coded 24h change

---

## FUTURE DEVELOPMENTS
- [ ] Dockerize the pipeline and database
- [ ] Replace APScheduler with Apache Airflow
- [ ] Add data quality checks with Great Expectations
- [ ] Add dbt models for cleaned views on top of raw data
- [ ] Deploy dashboard to Streamlit Cloud

---
