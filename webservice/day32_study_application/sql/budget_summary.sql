SELECT
    COUNT(*) AS total_count,
    COALESCE(SUM(balance), 0) AS total_balance
FROM budget_plans;