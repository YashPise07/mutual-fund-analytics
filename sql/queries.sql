# Top 5 funds by AUM

SELECT fund_name, aum
FROM dim_fund
ORDER BY aum DESC
LIMIT 5;

# Average NAV per month

SELECT
    strftime('%Y-%m', date) AS month,
    AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY month;

# Transactions by state

SELECT state, COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state;

#fund with expense ratio less than 1%

SELECT fund_name, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1;


