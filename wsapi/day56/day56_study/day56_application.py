# day56_application.py
# Application: 학과 세미나 신청 PostgreSQL API

# 요구사항
# 세미나 신청 이력을 PostgreSQL에 저장합니다.
# seminar_signups(id, seminar_name, attendee, status, created_at) 생성
# POST /signups, GET /signups, PATCH /signups/{id}, DELETE /signups/{id}
# status는 requested/confirmed/cancelled 중 하나입니다.
# psycopg 파라미터 바인딩, Depends, commit, 404 처리를 사용합니다.
# DB 연결 문자열은 DATABASE_URL 환경변수를 사용합니다.

import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Literal
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', '').strip()

signup_router = APIRouter(
    prefix='/signups',
    tags=['signups']
)

class SignupCreate(BaseModel):
    seminar_name: str = Field(min_length=1, max_length=100)
    attendee: str = Field(min_length=1, max_length=50)

class SignupPatch(BaseModel):
    status: Literal['requested', 'confirmed', 'cancelled']

class SignupOut(SignupCreate):
    id: int
    status: Literal['requested', 'confirmed', 'cancelled']
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

def db_connection():
    if not DATABASE_URL:
        raise HTTPException(503, 'DATABASE_URL을 설정해야 합니다.')

    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            yield conn
    except psycopg.OperationalError as exc:
        raise HTTPException(503, '데이터베이스 연결 실패') from exc

def initialize_schema():
    if not DATABASE_URL:
        raise RuntimeError('DATABASE_URL을 읽지 못했습니다.')

    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS SEMINAR_SIGNUPS (
                ID BIGSERIAL PRIMARY KEY,
                SEMINAR_NAME VARCHAR(100) NOT NULL,
                ATTENDEE VARCHAR(50) NOT NULL,
                STATUS VARCHAR(10) NOT NULL DEFAULT 'requested',
                CREATED_AT TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                CHECK (STATUS IN ('requested', 'confirmed', 'cancelled'))
            )
        ''')

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_schema()
    yield

app = FastAPI(
    lifespan=lifespan,
    title='학과 세미나 신청 API',
    version='0.0.1'
)

def create_signup_service(conn, data):
    row = conn.execute('''
        INSERT INTO SEMINAR_SIGNUPS (SEMINAR_NAME, ATTENDEE)
        VALUES (%s, %s)
        RETURNING *
    ''', (data.seminar_name, data.attendee)).fetchone()

    conn.commit()
    return row

def list_signups_service(conn):
    return conn.execute('''
        SELECT *
        FROM SEMINAR_SIGNUPS
        ORDER BY ID DESC
    ''').fetchall()

def update_signup_service(conn, signup_id, data):
    row = conn.execute('''
        UPDATE SEMINAR_SIGNUPS
        SET STATUS = %s
        WHERE ID = %s
        RETURNING *
    ''', (data.status, signup_id)).fetchone()
    conn.commit()
    return row

def delete_signup_service(conn, signup_id):
    row = conn.execute('''
        DELETE FROM SEMINAR_SIGNUPS
        WHERE ID = %s
        RETURNING ID
    ''', (signup_id,)).fetchone()

    conn.commit()
    return row is not None

# POST /signups: 세미나 신청을 생성하고 201 반환
@signup_router.post('', response_model=SignupOut, status_code=201)
def create_signup(data: SignupCreate, conn=Depends(db_connection)):
    return create_signup_service(conn, data)

# GET /signups: 전체 세미나 신청 목록 반환
@signup_router.get('', response_model=list[SignupOut])
def list_signups(conn=Depends(db_connection)):
    return list_signups_service(conn)

# PATCH /signups/{id}: 신청 상태 변경, 없는 ID는 404
@signup_router.patch('/{signup_id}', response_model=SignupOut)
def update_signup(
    signup_id: int,
    data: SignupPatch,
    conn=Depends(db_connection)
):
    signup = update_signup_service(conn, signup_id, data)

    if signup is None:
        raise HTTPException(404, '해당 세미나 신청이 없습니다.')

    return signup

# DELETE /signups/{id}: 신청 삭제, 없는 ID는 404
@signup_router.delete('/{signup_id}')
def delete_signup(signup_id: int, conn=Depends(db_connection)):
    if not delete_signup_service(conn, signup_id):
        raise HTTPException(404, '해당 세미나 신청이 없습니다.')

    return {'deleted': True, 'id': signup_id}

app.include_router(signup_router)