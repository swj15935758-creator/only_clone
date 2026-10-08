# day29_ex1.py
# pip install "psycopg[binary]"
# 주제: PostgreSQL + psycopg CRUD 실습


import psycopg
from db import get_connection, load_sql
from util.print_util import pp

# 테이블 생성 함수
def create_table(conn):
    sql = load_sql('speaker_create_table.sql')
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit() # 커밋을 해야 데이터 베이스에 반영됨

# create_tale(get_connection())

# insert
def add_speaker(conn, name,language,sample_count):
    sql = load_sql('speaker_add_speaker.sql')
    with conn.cursor() as cur:
        cur.execute(sql, (name, language, sample_count))
        row = cur.fetchone()
        conn.commit()
        return row[0] # ID 반환

# result = add_speaker(get_connection(),'홍길동','한국어',300)
# result = add_speaker(get_connection(),'세종대왕','영어',500)
# result = add_speaker(get_connection(),'유관순','둑일어',700)
# pp(result)

# SELECT ALL
def get_speaker(conn):
    sql = load_sql('speaker_get_speaker.sql')
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall() # 전체 조회결과 행튜플들의 리스트 반환

# pp(get_speaker(get_connection()))

# 조건 SELECT
def get_speakers_by_language(conn, language):
    sql = load_sql('speaker_get_speakers_by_language.sql')
    with conn.cursor() as cur:
        cur.execute(sql, (language,))
        return cur.fetchall() # 조회된 행 반환

# pp(get_speakers_by_language(get_connection(), language='영어'))

# UPDATE
def update_sample_count(conn, speaker_id, sample_count):
    sql = load_sql('speaker_update_sample_count.sql')

    with conn.cursor() as cur:
        cur.execute(sql, (speaker_id, sample_count))
        conn.commit()

        return cur.rowcount

# rcount = update_sample_count(get_connection(), 1, 150)
# pp(rcount)

# DELETE
def delete_speaker(conn, speaker_id):
    sql = load_sql('speaker_delete.sql')
    with conn.cursor() as cur:
        cur.execute(sql, (speaker_id,))
        conn.commit()
        return cur.rowcount
# rcount = delete_speaker(get_connection(), 1)
# pp(rcount)

''' postgres
-- 한줄 주석
/*
 	여러줄 주석
 */

-- 실행 : Ctrl + Enter
-- TEST 테이블생성
-- 줄복사 : Ctrl + Alt + 아래 화살표
-- 줄삭제 : Shift + Del
create table TEST(
	TEST_ID SERIAL primary key,
	TEST_MSG varchar(50) not null
);


INSERT INTO TEST(TEST_MSG) VALUES ('hello');
INSERT INTO TEST(TEST_MSG) VALUES ('postgre');

select * from TEST;


commit
'''