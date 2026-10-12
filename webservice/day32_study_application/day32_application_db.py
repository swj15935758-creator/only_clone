# day32_application_db.py
import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

SQL_DIR = Path(__file__).resolve().parent / 'sql'


def execute(name, params=()):
    url = os.getenv('DATABASE_URL', '').strip()

    if not url:
        raise ValueError('DATABASE_URL .env 환경변수를 설정하세요.')

    sql = (SQL_DIR / name).read_text(encoding='utf-8')

    with psycopg.connect(
        url,
        connect_timeout=15,
        row_factory=dict_row
    ) as conn:
        return conn.execute(sql,params).fetchall()


def save_plan(title, result, request_key):
    title = title.strip()

    if not title or len(title) > 80:
        raise ValueError('계획 제목은 1~80자로 입력하세요.')

    rows = execute(
        'budget_save.sql',
        (
            title,
            result['income'],
            result['expense'],
            result['balance'],
            request_key
        )
    )

    return rows[0]['id'] if rows else None


def list_plans(keyword=''):
    return execute('budget_list.sql',(f'%{keyword.strip()}%',))


def get_plan(record_id):
    rows = execute('budget_detail.sql',(record_id,))
    return rows[0] if rows else None


def summary():
    return execute('budget_summary.sql')[0]