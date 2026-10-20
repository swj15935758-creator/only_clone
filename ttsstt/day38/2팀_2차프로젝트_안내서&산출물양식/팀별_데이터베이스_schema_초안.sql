-- 2팀 SQL 초안: 팀 설계에 맞게 수정하세요.
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS sentences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text TEXT NOT NULL,
    level SMALLINT NOT NULL CHECK (level BETWEEN 1 AND 3),
    category TEXT
);
CREATE TABLE IF NOT EXISTS practice_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sentence_id UUID NOT NULL REFERENCES sentences(id),
    transcript TEXT,
    wer DOUBLE PRECISION,
    cer DOUBLE PRECISION,
    latency_ms INTEGER,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS error_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID NOT NULL REFERENCES practice_runs(id) ON DELETE CASCADE,
    error_type TEXT NOT NULL,
    reference_token TEXT,
    hypothesis_token TEXT,
    position INTEGER
);
