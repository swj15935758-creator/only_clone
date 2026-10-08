SELECT id, model_name, accuracy
FROM model_runs
WHERE accuracy >= %s
ORDER BY accuracy DESC