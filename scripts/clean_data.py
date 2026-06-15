import pandas as pd
import os

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

print("Cleaning Process Started...")

# =========================
# LOAD DATASETS
# =========================
fund_master = pd.read_csv(os.path.join(RAW_DIR, "fund_master.csv"))
nav_history = pd.read_csv(os.path.join(RAW_DIR, "nav_history.csv"))
scheme_performance = pd.read_csv(os.path.join(RAW_DIR, "scheme_performance.csv"))
investor_transactions = pd.read_csv(os.path.join(RAW_DIR, "investor_transactions.csv"))

print("\nRaw Shapes:")
print("fund_master:", fund_master.shape)
print("nav_history:", nav_history.shape)
print("scheme_performance:", scheme_performance.shape)
print("investor_transactions:", investor_transactions.shape)

# Optional: standardize column names for all tables
def standardize_columns(df):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

fund_master = standardize_columns(fund_master)
nav_history = standardize_columns(nav_history)
scheme_performance = standardize_columns(scheme_performance)
investor_transactions = standardize_columns(investor_transactions)

# =========================
# CLEAN fund_master
# =========================
print("\nCleaning fund_master...")

fund_master = fund_master.drop_duplicates()
fund_master = fund_master.dropna(how="all")

if "launch_date" in fund_master.columns:
    fund_master["launch_date"] = pd.to_datetime(fund_master["launch_date"], errors="coerce")

for col in ["exit_load_pct", "expense_ratio_pct", "min_lumpsum_amount", "min_sip_amount"]:
    if col in fund_master.columns:
        fund_master[col] = pd.to_numeric(fund_master[col], errors="coerce")

fund_master.to_csv(os.path.join(PROCESSED_DIR, "clean_fund_master.csv"), index=False)
print("fund_master cleaned:", fund_master.shape)

# =========================
# CLEAN nav_history
# =========================
print("\nCleaning nav_history...")

if "date" in nav_history.columns:
    nav_history["date"] = pd.to_datetime(nav_history["date"], errors="coerce")

if "nav" in nav_history.columns:
    nav_history["nav"] = pd.to_numeric(nav_history["nav"], errors="coerce")

if "amfi_code" in nav_history.columns and "date" in nav_history.columns:
    nav_history = nav_history.sort_values(by=["amfi_code", "date"])
else:
    nav_history = nav_history.sort_values(by=nav_history.columns.tolist())

nav_history = nav_history.drop_duplicates()

# Forward fill NAV within each fund
if "amfi_code" in nav_history.columns and "nav" in nav_history.columns:
    nav_history["nav"] = nav_history.groupby("amfi_code")["nav"].ffill()
elif "nav" in nav_history.columns:
    nav_history["nav"] = nav_history["nav"].ffill()

if "nav" in nav_history.columns:
    nav_history = nav_history[nav_history["nav"].notna()]
    nav_history = nav_history[nav_history["nav"] > 0]

nav_history.to_csv(os.path.join(PROCESSED_DIR, "clean_nav_history.csv"), index=False)
print("nav_history cleaned:", nav_history.shape)

# =========================
# CLEAN scheme_performance
# =========================
print("\nCleaning scheme_performance...")

scheme_performance = scheme_performance.drop_duplicates()

# Convert known numeric columns if present
numeric_cols = [
    "returns_1yr", "returns_3yr", "returns_5yr",
    "expense_ratio", "expense_ratio_pct",
    "sharpe_ratio", "alpha", "beta", "volatility",
    "aum", "aum_crore", "max_drawdown", "max_drawdown_pct",
    "benchmark_3yr_pct"
]
for col in numeric_cols:
    if col in scheme_performance.columns:
        scheme_performance[col] = pd.to_numeric(scheme_performance[col], errors="coerce")

# If expense ratio column exists, keep reasonable values only
if "expense_ratio_pct" in scheme_performance.columns:
    scheme_performance = scheme_performance[
        (scheme_performance["expense_ratio_pct"].isna()) |
        ((scheme_performance["expense_ratio_pct"] >= 0.1) & (scheme_performance["expense_ratio_pct"] <= 2.5))
    ]
elif "expense_ratio" in scheme_performance.columns:
    scheme_performance = scheme_performance[
        (scheme_performance["expense_ratio"].isna()) |
        ((scheme_performance["expense_ratio"] >= 0.1) & (scheme_performance["expense_ratio"] <= 2.5))
    ]

scheme_performance.to_csv(
    os.path.join(PROCESSED_DIR, "clean_scheme_performance.csv"),
    index=False
)
print("scheme_performance cleaned:", scheme_performance.shape)

# =========================
# CLEAN investor_transactions
# =========================
print("\nCleaning investor_transactions...")

investor_transactions = investor_transactions.drop_duplicates()

# Standardize text columns safely
for col in investor_transactions.columns:
    if investor_transactions[col].dtype == "object":
        investor_transactions[col] = investor_transactions[col].astype(str).str.strip()

# Convert date
if "transaction_date" in investor_transactions.columns:
    investor_transactions["transaction_date"] = pd.to_datetime(
        investor_transactions["transaction_date"], errors="coerce"
    )

# Standardize transaction type
if "transaction_type" in investor_transactions.columns:
    investor_transactions["transaction_type"] = (
        investor_transactions["transaction_type"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

# Handle amount column name safely
amount_col = None
if "amount_inr" in investor_transactions.columns:
    amount_col = "amount_inr"
elif "amount" in investor_transactions.columns:
    amount_col = "amount"

if amount_col:
    investor_transactions[amount_col] = pd.to_numeric(
        investor_transactions[amount_col],
        errors="coerce"
    )
    investor_transactions = investor_transactions[investor_transactions[amount_col].notna()]
    investor_transactions = investor_transactions[investor_transactions[amount_col] > 0]

# Standardize KYC column name if needed
if "kyc_status" not in investor_transactions.columns and "kyc status" in investor_transactions.columns:
    investor_transactions = investor_transactions.rename(columns={"kyc status": "kyc_status"})

# Clean KYC values only if column exists
if "kyc_status" in investor_transactions.columns:
    investor_transactions["kyc_status"] = (
        investor_transactions["kyc_status"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    valid_kyc = {"VERIFIED", "PENDING", "REJECTED"}

    # Keep only rows that match valid KYC values, but only if matches exist
    matched_rows = investor_transactions["kyc_status"].isin(valid_kyc).sum()
    print("KYC matched rows:", matched_rows)

    if matched_rows > 0:
        investor_transactions = investor_transactions[
            investor_transactions["kyc_status"].isin(valid_kyc)
        ]
    else:
        print("Warning: No KYC values matched the valid list. Skipping KYC filter.")

# Drop rows with missing essential fields if present
essential_cols = [col for col in ["investor_id", "amfi_code", "transaction_date"] if col in investor_transactions.columns]
if essential_cols:
    investor_transactions = investor_transactions.dropna(subset=essential_cols)

# Final cleanup
investor_transactions = investor_transactions.reset_index(drop=True)

print("investor_transactions cleaned:", investor_transactions.shape)
print("\nInvestor Transactions Columns:")
print(investor_transactions.columns.tolist())
print("\nInvestor Transactions Preview:")
print(investor_transactions.head())

investor_transactions.to_csv(
    os.path.join(PROCESSED_DIR, "clean_investor_transactions.csv"),
    index=False
)

print("\nAll datasets cleaned successfully.")