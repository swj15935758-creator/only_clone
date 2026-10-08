INSERT INTO model_runs (
    model_name, dataset_name, accuracy, epochs, memo
)
VALUES (%s, %s, %s, %s, %s)
RETURNING id