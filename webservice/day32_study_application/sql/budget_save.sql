INSERT INTO budget_plans
    (title, income, expense, balance, request_key)
VALUES
    (%s, %s, %s, %s, %s)
ON CONFLICT (request_key) DO NOTHING
RETURNING id;