import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException,APIRouter
from pydantic import BaseModel,Field

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = FastAPI(title='세미나 신청 API')

router = APIRouter(prefix='/signups',tags=['signups'])

class SignupIn(BaseModel):
    seminar_name: str = Field(min_length=2,max_length=100)
    attendee: str = Field(min_length=2,max_length=50)

class SignupPatch(BaseModel):
    status: str = Field(pattern='^(requested|confirmed|cancelled)$')

def get_db():
    if not DATABASE_URL:
        raise HTTPException(status_code=503, detail="Database 미설정")
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            yield conn
    except psycopg.OperationalError:
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.on_event('startup')
def prepare_database():
    if not DATABASE_URL:
        return
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS SEMINAR_SIGNUPS
        (
            ID
            BIGSERIAL
            PRIMARY
            KEY,
            SEMINAR_NAME
            VARCHAR
        (
            100
        ) NOT NULL,
            ATTENDEE VARCHAR
        (
            100
        ) NOT NULL,
            STATUS VARCHAR
        (
            15
        ) NOT NULL DEFAULT 'requested',
            CREATED_AT TIMESTAMPTZ NOT NULL DEFAULT NOW
        (
        )
            )
            
        ''')

@router.post('', status_code=201)
def add_signups(data: SignupIn, conn=Depends(get_db)):
    row = conn.execute('''
        INSERT INTO SEMINAR_SIGNUPS (SEMINAR_NAME, ATTENDEE)
            VALUES (%s, %s)
            RETURNING *
    ''', (data.seminar_name, data.attendee)).fetchone()
    conn.commit()
    return row

@router.get('')
def all_signups(conn=Depends(get_db)):
    return conn.execute('''
    SELECT * FROM SEMINAR_SIGNUPS 
    ORDER BY ID
    ''').fetchall()

@router.patch('/{signup_id}')
def change_status(signup_id: int, data: SignupPatch, conn=Depends(get_db)):
    row = conn.execute('''
    UPDATE SEMINAR_SIGNUPS
    SET STATUS = %s
    WHERE ID = %s
    RETURNING *
    ''',(data.status, signup_id)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="신청 기록 없음")
    conn.commit()
    return row

@router.delete('/{signup_id}')
def remove_signup(signup_id: int, conn=Depends(get_db)):
    row =conn.execute('''
    DELETE FROM SEMINAR_SIGNUPS
    WHERE ID = %s
    RETURNING *
    ''',(signup_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="신청 기록 없음")
    conn.commit()
    return {'deleted': True}

app.include_router(router)
