import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent / 'sql'
if not SQL_DIR.exists():
    SQL_DIR.mkdir(parents=True, exist_ok=True)

def load_sql(filename):
    path = (SQL_DIR / filename).resolve()
    if path.parent != SQL_DIR.resolve() or path.suffix != '.sql':
        raise ValueError('sql폴더의 .sql파일명만 지정하세요.')
    return path.read_text(encoding='utf-8')

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def has_database_url():
    return bool(DATABASE_URL)

def get_connection():
    if not has_database_url():
        raise ValueError("DATABASE_URL이 설정되지 않았습니다!")
    return psycopg.connect(DATABASE_URL)

def create_table():
    sql = load_sql('create_table_application.sql')
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

def save_job_application(company, position, status, memo):
    sql = load_sql('save_job_application.sql')
    params = (company, position, status, memo or None)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()[0]

def load_job_applications(keyword=''):
    sql = load_sql('load_job_application.sql')
    params = (f'%{keyword.strip()}%',)

    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()

def update_job_application_status(application_id, status):
    sql = load_sql('update_job_application.sql')
    params = (status, application_id)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount
