import os
import psycopg
from psycopg.rows import dict_row # 조회한 행들을 딕셔너리로 가져오는 함수
from dotenv import load_dotenv # .env 로딩 라이브러리
from pathlib import Path

# SQL 파일들 저장 디렉토리
SQL_DIR = Path(__file__).resolve().parent / 'sql'
if not SQL_DIR.exists(): # 디렉토리 없다면
    SQL_DIR.mkdir(parents=True, exist_ok=True) # 새로 생성

# 파일명에 해당하는 SQL 문자열을 리턴하는 함수
def load_sql(filename):
    path = (SQL_DIR / filename).resolve() # SQL파일의 서버상의 실제경로
    # 생성된 sql디렉토리에 SQL파일이 없거나 SQL파일의 확장자가 sql이 아니라면
    if path.parent != SQL_DIR.resolve() or path.suffix != '.sql':
        raise ValueError('sql폴더의 .sql파일명만 지정하세요.')
    return path.read_text(encoding='utf-8') # SQL파일내의 문자열을 리턴

# .env 파일의 환경 변수를 로딩
load_dotenv()
# 메모리에 로딩된 .env 파일의 DATABASE_URL 환경변수의 값 저장
DATABASE_URL = os.getenv("DATABASE_URL")
# pp(DATABASE_URL)

# DATABASE_UTL 유효여부 확인하는 함수
def has_database_url():
    return bool(DATABASE_URL)

# Connection 획득 함수
def get_connection():
    if not has_database_url():
        raise ValueError("DATABASE_URL이 설정되지 않았습니다!")
    return psycopg.connect(DATABASE_URL)

# 테이블 생성 함수
def create_table():
    sql = load_sql('create_table_basic.sql')
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

def save_study_schedule(subject,study_date,place):
    sql = load_sql('save_study_schedule_basic.sql')
    params = (subject,study_date,place)
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()[0]

def load_study_schedule():
    sql = load_sql('load_study_schedule_basic.sql')
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()