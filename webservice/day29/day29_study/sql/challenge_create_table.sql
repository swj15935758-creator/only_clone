CREATE TABLE IF NOT EXISTS model_runs (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(80) NOT NULL,
    dataset_name VARCHAR(80) NOT NULL,
    accuracy NUMERIC(5, 4) NOT NULL, -- 전체 5자리, 소수이하 4자리
    epochs INTEGER NOT NULL,
    memo TEXT
)