from sqlalchemy import create_engine
import pandas as pd
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database path
DB_PATH = os.path.join(BASE_DIR, "..", "bluestock_mf.db")

# SQLite connection
engine = create_engine(f"sqlite:///{DB_PATH}")

print("Database Connected")

# Processed data folder
PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed"
)

# =========================
# LOAD CLEANED FILES
# =========================

fund_master = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_fund_master.csv")
)

nav_history = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_nav_history.csv")
)

scheme_performance = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_scheme_performance.csv")
)

investor_transactions = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_investor_transactions.csv")
)

# =========================
# LOAD TABLES INTO SQLITE
# =========================

fund_master.to_sql(
    "dim_fund",
    engine,
    if_exists="replace",
    index=False
)

nav_history.to_sql(
    "fact_nav",
    engine,
    if_exists="replace",
    index=False
)

scheme_performance.to_sql(
    "fact_performance",
    engine,
    if_exists="replace",
    index=False
)

investor_transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="replace",
    index=False
)

print("All tables loaded successfully.")