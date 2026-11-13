# day56_basic.py
# 주제 Basic: 도서 대출 예약 API

import os
from contextlib import asynccontextmanager
from datetime import datetime

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL', '')

library_router = APIRouter(
    prefix='/reservations',
    tags=['library']
)

class LoanCreate(BaseModel):
    book_title: str = Field(min_length=2, max_length=80)
    reservation_name: str = Field(min_length=2, max_length=30)

class LoanOut(LoanCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

def db_connection(): # db 연결 함수
    if not DATABASE_URL:
        raise HTTPException(503, 'DATABASE_URL을 설정해야 합니다.')

    try:
        # 조회한 행을 딕셔너리로 가져오는 데이터베이스 커넥션
        # with가 끝나면 데이터베이스 커넥션도 종료
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            yield conn # 라우터로 연결 객체 전달
    except psycopg.OperationalError:
        raise HTTPException(503, '데이터베이스 연결 실패')

# 테이블 생성 함수
def initialize_schema():
    if not DATABASE_URL:
        raise RuntimeError('DATABASE_URL을 읽지 못했습니다.')

    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS LIBRARY_LOAN (
            ID BIGSERIAL PRIMARY KEY,
            BOOK_TITLE VARCHAR(80) NOT NULL,
            RESERVATION_NAME VARCHAR(30) NOT NULL,
            CREATED_AT TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        ''')

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_schema()
    yield

app = FastAPI(
    lifespan=lifespan,
    title='도서 대출 예약 API',
    version='0.0.1'
)

def create_reservations_service(conn, data):
    row = conn.execute('''
        INSERT INTO LIBRARY_LOAN (BOOK_TITLE, RESERVATION_NAME)
        VALUES (%s, %s)
        RETURNING *
    ''', (data.book_title, data.reservation_name)).fetchone()

    conn.commit()
    return row

def list_reservations_service(conn, limit, offset):
    return conn.execute('''
        SELECT *
        FROM LIBRARY_LOAN
        ORDER BY ID DESC
        LIMIT %s
        OFFSET %s
    ''', (limit, offset)).fetchall()

def reservation_service(conn, reservation_id):
    return conn.execute('''
        SELECT *
        FROM LIBRARY_LOAN
        WHERE ID = %s
    ''', (reservation_id,)).fetchone()

def delete_reservation_service(conn, reservation_id):
    row = conn.execute('''
        DELETE FROM LIBRARY_LOAN
        WHERE ID = %s
        RETURNING ID
    ''', (reservation_id,)).fetchone()

    conn.commit()
    return row is not None

# 요구사항 1~7 > id, 도서명, 예약자명
# 1. 작업 관리·미디어 처리 주제와 다른 도서 예약 서비스를 FastAPI로 구현합니다.
# 2. POST /reservations : 도서명, 예약자명을 받아 고유 정수 ID로 저장합니다.
@library_router.post('', response_model=LoanOut, status_code=201)
def create_reservations(data: LoanCreate, conn=Depends(db_connection)):
    return create_reservations_service(conn, data)

# 3. GET /reservations : 전체 예약 목록을 반환합니다.
@library_router.get('', response_model=list[LoanOut])
def list_reservations(
    limit: int | None = Query(None, ge=1, le=100),
    offset: int = Query(0, ge=0),
    conn=Depends(db_connection)
):
    return list_reservations_service(conn, limit, offset)

# 4. GET /reservations/{id} : 한 건 조회하고 없으면 404를 반환합니다.
@library_router.get('/{reservation_id}', response_model=LoanOut)
def get_reservation(reservation_id: int,conn=Depends(db_connection)):
    loan = reservation_service(conn, reservation_id)

    if loan is None:
        raise HTTPException(404, '해당 데이터가 없습니다.')

    return loan

# 5. DELETE /reservations/{id} : 예약을 삭제하고 없으면 404를 반환합니다.
@library_router.delete('/{reservation_id}')
def delete_reservation(
    reservation_id: int,
    conn=Depends(db_connection)
):
    if not delete_reservation_service(conn, reservation_id):
        raise HTTPException(404, '해당 데이터가 없습니다.')

    return {'deleted': True, 'id': reservation_id}

# 6. APIRouter, BaseModel, Field를 사용합니다.
# 7. 도서명 2~80자, 예약자명 2~30자를 검증합니다.

app.include_router(library_router)