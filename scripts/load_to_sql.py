from sqlalchemy import create_engine
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "..", "bluestock_mf.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

print("Database Connected")
fund_master = pd.read_csv(
    os.path.join(BASE_DIR, "..", "data", "processed", "clean_fund_master.csv")
)

fund_master.to_sql(
    "dim_fund",
    engine,
    if_exists='replace',
    index=False
)

print("dim_fund Loaded")