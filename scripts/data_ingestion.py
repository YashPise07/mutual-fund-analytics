import pandas as pd
import os

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create path to data/raw
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "raw")

print("Data Path:")
print(DATA_PATH)

# Check if folder exists
if not os.path.exists(DATA_PATH):
    print("ERROR: data/raw folder not found")
    exit()

files = os.listdir(DATA_PATH)

print("\nCSV Files Found:")
print(files)

for file in files:

    if file.endswith(".csv"):

        file_path = os.path.join(DATA_PATH, file)

        print("\n========================")
        print(f"Reading File: {file}")

        # Load CSV
        df = pd.read_csv(file_path)

        # Basic Information
        print("\nShape:")
        print(df.shape)

        print("\nColumns:")
        print(df.columns)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        # Data Quality Check
        print("\nData Quality Summary")

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:")
        print(df.duplicated().sum())

        # Optional Checks
        # Only run if columns exist
        if 'fund_house' in df.columns:
            print("\nUnique Fund Houses:")
            print(df['fund_house'].unique())

        if 'scheme_category' in df.columns:
            print("\nScheme Categories:")
            print(df['scheme_category'].value_counts())

        if 'risk_grade' in df.columns:
            print("\nRisk Grades:")
            print(df['risk_grade'].value_counts())