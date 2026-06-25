import os
import numpy as np
import pandas as pd

# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed"
)

REPORTS_DIR = os.path.join(
    BASE_DIR,
    "..",
    "reports"
)

os.makedirs(REPORTS_DIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

scheme = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_scheme_performance.csv")
)

nav = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_nav_history.csv")
)

nav["date"] = pd.to_datetime(nav["date"])

print("Datasets Loaded Successfully")
print("Scheme Shape :", scheme.shape)
print("NAV Shape    :", nav.shape)

# ============================================================
# DAILY RETURNS
# ============================================================

nav = nav.sort_values(["amfi_code", "date"])

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

# ============================================================
# RISK FREE RATE
# ============================================================

RISK_FREE = 0.065

# ============================================================
# CALCULATE METRICS
# ============================================================

metrics = []

for fund in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == fund
    ].copy()

    returns = temp["daily_return"].dropna()

    if len(returns) < 30:
        continue

    # Annual Return
    annual_return = returns.mean() * 252

    # Annual Volatility
    annual_std = returns.std() * np.sqrt(252)

    # Sharpe Ratio
    if annual_std != 0:
        sharpe = (annual_return - RISK_FREE) / annual_std
    else:
        sharpe = np.nan

    # Sortino Ratio
    downside = returns[returns < 0]

    if len(downside) > 0:
        downside_std = downside.std() * np.sqrt(252)

        if downside_std != 0:
            sortino = (annual_return - RISK_FREE) / downside_std
        else:
            sortino = np.nan
    else:
        sortino = np.nan

    # Beta
    beta = scheme.loc[
        scheme["amfi_code"] == fund,
        "beta"
    ]

    beta = beta.iloc[0] if len(beta) else np.nan

    # Alpha
    alpha = scheme.loc[
        scheme["amfi_code"] == fund,
        "alpha"
    ]

    alpha = alpha.iloc[0] if len(alpha) else np.nan

    # AUM
    aum = scheme.loc[
        scheme["amfi_code"] == fund,
        "aum_crore"
    ]

    aum = aum.iloc[0] if len(aum) else np.nan

    # Expense Ratio
    expense = scheme.loc[
        scheme["amfi_code"] == fund,
        "expense_ratio_pct"
    ]

    expense = expense.iloc[0] if len(expense) else np.nan

    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()

    running_max = cumulative.cummax()

    drawdown = (
        cumulative - running_max
    ) / running_max

    max_drawdown = drawdown.min()

    metrics.append({

        "amfi_code": fund,

        "Annual Return": round(annual_return * 100, 2),

        "Annual Volatility": round(annual_std * 100, 2),

        "Sharpe Ratio": round(sharpe, 3),

        "Sortino Ratio": round(sortino, 3),

        "Alpha": round(alpha, 3),

        "Beta": round(beta, 3),

        "Maximum Drawdown": round(max_drawdown * 100, 2),

        "AUM (Crore)": round(aum, 2),

        "Expense Ratio (%)": round(expense, 2)

    })

# ============================================================
# CREATE SCORECARD
# ============================================================

scorecard = pd.DataFrame(metrics)

scorecard = scorecard.sort_values(
    by="Sharpe Ratio",
    ascending=False
)

# ============================================================
# SAVE CSV
# ============================================================

output_path = os.path.join(
    REPORTS_DIR,
    "fund_scorecard.csv"
)

scorecard.to_csv(
    output_path,
    index=False
)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========== TOP 10 FUNDS ==========\n")

print(scorecard.head(10))

print("\nSaved Successfully")

print(output_path)