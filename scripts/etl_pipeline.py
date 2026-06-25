import os

print("========== ETL PIPELINE ==========\n")

print("Step 1 : Data Ingestion")
os.system("python scripts/data_ingestion.py")

print("\nStep 2 : Live NAV Fetch")
os.system("python scripts/live_nav_fetch.py")

print("\nStep 3 : Data Cleaning")
os.system("python scripts/clean_data.py")

print("\nETL Pipeline Completed Successfully!")