import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
funds = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_scheme_performance.csv")
)

nav = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_nav_history.csv")
)

investors = pd.read_csv(
    os.path.join(PROCESSED_DIR, "clean_investor_transactions.csv")
)
print(funds.shape)
print(nav.shape)
print(investors.shape)


nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(
    ["amfi_code","date"]
)

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

var_data = []

for fund in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == fund
    ]

    returns = temp["daily_return"].dropna()

    if len(returns) > 0:

        var95 = np.percentile(
            returns,
            5
        )

        var_data.append(
            [fund,var95]
        )

var_df = pd.DataFrame(
    var_data,
    columns=["amfi_code","VaR_95"]
)

print(var_df.head())

cvar_list = []

for fund in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == fund
    ]

    returns = temp["daily_return"].dropna()

    if len(returns) > 0:

        var95 = np.percentile(
            returns,
            5
        )

        cvar = returns[
            returns <= var95
        ].mean()

        cvar_list.append(
            [fund,cvar]
        )

cvar_df = pd.DataFrame(
    cvar_list,
    columns=["amfi_code","CVaR"]
)

report = pd.merge(
    var_df,
    cvar_df,
    on="amfi_code"
)

report.to_csv(
    os.path.join(REPORTS_DIR, "var_cvar_report.csv"),
    index=False
)

print(report.head())

fund = nav["amfi_code"].iloc[0]

temp = nav[
    nav["amfi_code"] == fund
].copy()

risk_free = 0.065

temp["rolling_sharpe"] = (

    temp["daily_return"]
    .rolling(90)
    .mean()

    /

    temp["daily_return"]
    .rolling(90)
    .std()

) * np.sqrt(252)

plt.figure(figsize=(12,6))

plt.plot(
    temp["date"],
    temp["rolling_sharpe"]
)

plt.title(
    "90 Day Rolling Sharpe Ratio"
)

plt.grid()

plt.savefig(
    os.path.join(REPORTS_DIR, "rolling_sharpe_chart.png")
)
plt.show()

investors["transaction_date"] = pd.to_datetime(
    investors["transaction_date"],
    errors="coerce"
)

investors["cohort_year"] = (
    investors["transaction_date"]
    .dt.year
)

cohort = investors.groupby(
    "cohort_year"
).agg({

    "amount_inr":"sum",
    "investor_id":"nunique"

}).reset_index()

print(cohort)

sip = investors[
    investors["transaction_type"]=="SIP"
]

continuity = sip.groupby(
    "investor_id"
).size()

continuous = continuity[
    continuity >= 6
]

print(
    "Continuous SIP Investors:",
    len(continuous)
)

