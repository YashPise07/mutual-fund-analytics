import pandas as pd
import os

# =========================
# PATH SETUP
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")

PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

# Create processed folder
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Cleaning Process Started...")

# =========================
# LOAD DATASETS
# =========================

fund_master = pd.read_csv(
    os.path.join(RAW_DIR, "fund_master.csv")
)

nav_history = pd.read_csv(
    os.path.join(RAW_DIR, "nav_history.csv")
)

scheme_performance = pd.read_csv(
    os.path.join(RAW_DIR, "scheme_performance.csv")
)

investor_transactions = pd.read_csv(
    os.path.join(RAW_DIR, "investor_transactions.csv")
)

# =========================
# CLEAN fund_master
# =========================

print("\nCleaning fund_master...")

fund_master.drop_duplicates(inplace=True)

fund_master.dropna(how='all', inplace=True)

# Save cleaned file
fund_master.to_csv(
    os.path.join(PROCESSED_DIR, "clean_fund_master.csv"),
    index=False
)

print("fund_master cleaned.")

# =========================
# CLEAN nav_history
# =========================

print("\nCleaning nav_history...")

# Convert date
nav_history['date'] = pd.to_datetime(
    nav_history['date'],
    errors='coerce'
)

# Sort values
nav_history = nav_history.sort_values(
    by=['amfi_code', 'date']
)

# Remove duplicates
nav_history.drop_duplicates(inplace=True)

# Fill missing NAV values
nav_history['nav'] = nav_history['nav'].ffill()

# Convert NAV to float
nav_history['nav'] = pd.to_numeric(
    nav_history['nav'],
    errors='coerce'
)

# Keep valid NAV only
nav_history = nav_history[
    nav_history['nav'] > 0
]

# Save cleaned file
nav_history.to_csv(
    os.path.join(PROCESSED_DIR, "clean_nav_history.csv"),
    index=False
)

print("nav_history cleaned.")

# =========================
# CLEAN scheme_performance
# =========================

print("\nCleaning scheme_performance...")

scheme_performance.drop_duplicates(inplace=True)

# Convert returns to numeric
if 'returns_1yr' in scheme_performance.columns:

    scheme_performance['returns_1yr'] = pd.to_numeric(
        scheme_performance['returns_1yr'],
        errors='coerce'
    )

# Validate expense ratio
if 'expense_ratio' in scheme_performance.columns:

    scheme_performance = scheme_performance[
        (scheme_performance['expense_ratio'] >= 0.1) &
        (scheme_performance['expense_ratio'] <= 2.5)
    ]

# Save cleaned file
scheme_performance.to_csv(
    os.path.join(PROCESSED_DIR, "clean_scheme_performance.csv"),
    index=False
)

print("scheme_performance cleaned.")

# =========================
# CLEAN investor_transactions
# =========================

print("\nCleaning investor_transactions...")

investor_transactions.drop_duplicates(inplace=True)

# Standardize transaction types
if 'transaction_type' in investor_transactions.columns:

    investor_transactions['transaction_type'] = (
        investor_transactions['transaction_type']
        .astype(str)
        .str.upper()
    )

# Validate amount
if 'amount' in investor_transactions.columns:

    investor_transactions = investor_transactions[
        investor_transactions['amount'] > 0
    ]

# Convert transaction date
if 'transaction_date' in investor_transactions.columns:

    investor_transactions['transaction_date'] = pd.to_datetime(
        investor_transactions['transaction_date'],
        errors='coerce'
    )

# Validate KYC status
if 'kyc_status' in investor_transactions.columns:

    valid_kyc = ['VERIFIED', 'PENDING', 'REJECTED']

    investor_transactions = investor_transactions[
        investor_transactions['kyc_status'].isin(valid_kyc)
    ]

# Save cleaned file
investor_transactions.to_csv(
    os.path.join(PROCESSED_DIR, "clean_investor_transactions.csv"),
    index=False
)

print("investor_transactions cleaned.")

print("\nAll datasets cleaned successfully.")