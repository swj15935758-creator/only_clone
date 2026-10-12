SELECT
    id,
    title,
    income,
    expense,
    balance
FROM budget_plans
WHERE title ILIKE %s
ORDER BY id DESC
LIMIT 100;