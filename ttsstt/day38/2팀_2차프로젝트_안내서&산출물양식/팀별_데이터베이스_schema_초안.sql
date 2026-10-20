-- 2팀 SQL 초안: 팀 설계에 맞게 수정하세요.

-- PostgreSQL 확장 기능 설치
CREATE EXTENSION IF NOT EXISTS pgcrypto; -- 암호화·해시 관련 확장 기능, 이미 존재하면 건너뜀

-- 연습 문장 저장 테이블
CREATE TABLE IF NOT EXISTS sentences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- 문장 고유 ID, UUID 자동 생성, 기본키(PK)
    text TEXT NOT NULL, -- 정답 문장, 반드시 입력
    level SMALLINT NOT NULL CHECK (level BETWEEN 1 AND 3), -- 난이도: 1=쉬움, 2=보통, 3=어려움
    category TEXT -- 문장 주제 또는 분류, NULL 허용
);

-- 사용자 연습 결과 저장 테이블
CREATE TABLE IF NOT EXISTS practice_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- 연습 기록 고유 ID, 자동 생성, 기본키(PK)
    sentence_id UUID NOT NULL REFERENCES sentences(id), -- 연습한 문장의 ID, sentences 테이블 참조(FK)
    transcript TEXT, -- STT로 인식한 문장
    wer DOUBLE PRECISION, -- 단어 오류율, 예: 0.25 = 25%
    cer DOUBLE PRECISION, -- 문자 오류율, 예: 0.10 = 10%
    latency_ms INTEGER, -- 음성 처리시간, 밀리초(ms) 단위
    status TEXT NOT NULL, -- 처리 상태, 예: success 또는 error
    created_at TIMESTAMPTZ NOT NULL DEFAULT now() -- 연습 날짜와 시간, 자동 생성
);

-- STT 전사 오류 상세 기록 테이블
CREATE TABLE IF NOT EXISTS error_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- 오류 기록 고유 ID, 자동 생성, 기본키(PK)
    run_id UUID NOT NULL REFERENCES practice_runs(id) ON DELETE CASCADE, -- 연습 기록 참조(FK), 연습 기록 삭제 시 관련 오류도 삭제
    error_type TEXT NOT NULL, -- 오류 종류: substitution(대체), deletion(삭제), insertion(삽입)
    reference_token TEXT, -- 정답 문장에 있는 단어 또는 어절
    hypothesis_token TEXT, -- STT가 인식한 단어 또는 어절
    position INTEGER -- 오류가 발생한 위치
);