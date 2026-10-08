# day29_application.py
# 주제:Application 과제 - 채용 공고 관리

from db import get_connection, load_sql
from util.print_util import pp

# 주제
# 채용 공고 데이터를 Python CRUD 함수로 관리합니다.

# 테이블명
# jobs

# 필수 컬럼
# id: 자동 증가 Primary Key
# company: 회사명
# position: 직무명
# location: 근무지역
# salary: 연봉
# status: 공고 상태

def create_job_table(conn):
    sql = load_sql('create_job_table.sql')
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def insert_job_data(conn, company, position, location, salary, status):
    sql = load_sql('insert_job_data.sql')
    with conn.cursor() as cur:
        cur.execute(sql,(company, position, location, salary, status))
        job_id = cur.fetchone()[0]
    conn.commit()
    return job_id


def select_jobs_data(conn):
    sql = load_sql('select_jobs_data.sql')
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows


def select_jobs_by_location(conn, location):
    sql = load_sql('select_jobs_by_location.sql')
    with conn.cursor() as cur:
        cur.execute(sql,(location,))
        rows = cur.fetchall()
    return rows


def update_job_salary(conn, job_id, salary):
    sql = load_sql('update_job_salary.sql')
    with conn.cursor() as cur:
        cur.execute(sql,(salary, job_id))
        row_count = cur.rowcount
    conn.commit()
    return row_count


def delete_job_data(conn, job_id):
    sql = load_sql('delete_job_data.sql')
    with conn.cursor() as cur:
        cur.execute(sql,(job_id,))
        row_count = cur.rowcount
    conn.commit()
    return row_count

def main():
    create_job_table(get_connection())
    pp('jobs 테이블 생성 완료')

    job_id1 = insert_job_data(get_connection(),'네이버','백엔드 개발자','서울',5000,'채용중')
    job_id2 = insert_job_data(get_connection(),'카카오','데이터 분석가','경기',4800,'채용중')
    job_id3 = insert_job_data(get_connection(),'라인','AI 개발자','서울',5500,'마감')

    pp(job_id1)
    pp(job_id2)
    pp(job_id3)
    pp(select_jobs_data(get_connection()))
    pp(select_jobs_by_location(get_connection(),'서울'))
    update_count = update_job_salary(get_connection(),job_id1,6000)
    pp(update_count)
    delete_count = delete_job_data(get_connection(),job_id2)
    pp(delete_count)


if __name__ == '__main__':
    main()