import requests
import pandas as pd
import os

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create path to data/raw
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "raw")

# Automatically create folder if missing
os.makedirs(DATA_DIR, exist_ok=True)

# Mutual fund scheme codes
schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 120841,
    "Kotak_Bluechip": 120841
}

# Loop through all schemes
for fund_name, scheme_code in schemes.items():

    print(f"\nFetching {fund_name}")

    # API URL
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    # API Request
    response = requests.get(url)

    # Convert JSON
    data = response.json()

    # Extract NAV data
    nav_data = data['data']

    # Create DataFrame
    df = pd.DataFrame(nav_data)

    # Create save path
    save_path = os.path.join(DATA_DIR, f"{fund_name}.csv")

    # Save CSV
    df.to_csv(save_path, index=False)

    print(f"Saved Successfully: {save_path}")

print("\nAll Mutual Fund NAV files downloaded successfully.")