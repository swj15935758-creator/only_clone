# day32_basic_db.py

import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

load_dotenv()

SQL_DIR = Path(__file__).resolve().parent / 'sql'

def execute(name,params = ()):
    url = os.getenv('DATABASE_URL','').strip()
    if not url:
        raise ValueError('DATABASE_URL .env 환경변수를 설정')
    sql = (SQL_DIR / name).read_text(encoding='utf-8')
    with psycopg.connect(
        url,
        connect_timeout=15,
        row_factory=dict_row
    )as conn:
        return conn.execute(sql,params).fetchall()

def save_run(label, result):
    label = label.strip()
    if not label or len(label) > 80:
        raise ValueError('견적 제목은 1~80자 이하로 입력하세요')

    rows = execute('save.sql',(
        label,
        result['weight'],
        result['fee'],
        result['rule_version'],
    ))
    return rows[0]['id'] if rows else None

def list_runs(keyword = ''):
    return execute('list.sql',(f'%{keyword.strip()}%',))