import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed"
)

funds = pd.read_csv(
    os.path.join(
        PROCESSED_DIR,
        "clean_scheme_performance.csv"
    )
)

print("\n========== FUND RECOMMENDER ==========")

risk = input(
    "\nEnter Risk Appetite (Low/Moderate/High): "
)

if risk.lower() == "low":

    result = funds[
        funds["risk_grade"].str.lower() == "low"
    ].sort_values(
        "sharpe_ratio",
        ascending=False
    ).head(3)

elif risk.lower() == "moderate":

    result = funds[
        funds["risk_grade"].str.lower() == "moderate"
    ].sort_values(
        "sharpe_ratio",
        ascending=False
    ).head(3)

elif risk.lower() == "high":

    result = funds[
        funds["risk_grade"].str.lower() == "high"
    ].sort_values(
        "sharpe_ratio",
        ascending=False
    ).head(3)

else:

    print("\nInvalid Input!")
    exit()

print("\nTop Recommended Funds:\n")

print(
    result[
        [
            "scheme_name",
            "fund_house",
            "risk_grade",
            "sharpe_ratio",
            "alpha",
            "aum_crore"
        ]
    ]
)