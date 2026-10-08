# day29_basic.py
# 주제:Basic 과제 - 도서 대여 관리
import os
import psycopg
from db import get_connection, load_sql
from util.print_util import pp, up
# 주제
# PostgreSQL에 도서 정보를 저장하고 기본 SQL CRUD를 실습합니다.

# 테이블명
# books

# 필수 컬럼
# id: 자동 증가 Primary Key
# title: 도서명, VARCHAR(100), NOT NULL
# author: 저자명, VARCHAR(50), NOT NULL
# stock: 보유 수량, INTEGER, 기본값 0
def create_book_table(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql('create_book_table.sql'))
        conn.commit()

create_book_table(get_connection())
pp('books 테이블 생성 완료')


def insert_book_data(conn, title, author, stock):
    sql = load_sql('insert_book_data.sql')
    with conn.cursor() as cur:
        cur.execute(sql, (title, author, stock))
        book_id = cur.fetchone()[0]
        conn.commit()
        return book_id

book_id1 = insert_book_data(get_connection(), '책', '신의진', 1)
book_id2 = insert_book_data(get_connection(), '책인가', '박세정', 5)
book_id3 = insert_book_data(get_connection(), '책일지도', '신박세의진정', 7)

pp(book_id1)
pp(book_id2)
pp(book_id3)


def select_books_data(conn):
    sql = load_sql('select_books_data.sql')
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

pp(select_books_data(get_connection()))


def select_books_by_stock(conn, min_stock):
    sql = load_sql('select_books_stock.sql')
    with conn.cursor() as cur:
        cur.execute(sql, (min_stock,))
        rows = cur.fetchall()

    return rows

pp(select_books_by_stock(get_connection(), 2))


def update_book_data(conn, book_id, stock):
    sql = load_sql('update_book_data.sql')

    with conn.cursor() as cur:
        cur.execute(sql, (stock, book_id))
        # UPDATE된 행의 개수
        row_count = cur.rowcount
    conn.commit()
    return row_count

pp(update_book_data(get_connection(), book_id1, 10))


def delete_book_data(conn, book_id):
    sql = load_sql('delete_book_data.sql')

    with conn.cursor() as cur:
        cur.execute(sql, (book_id,))
        # DELETE된 행의 개수
        row_count = cur.rowcount
    conn.commit()
    return row_count

pp(delete_book_data(get_connection(), book_id2))


# 요구사항
# books 테이블을 생성합니다.
# 서로 다른 도서 3권을 INSERT 합니다.
# 전체 도서를 SELECT 합니다.
# stock이 2 이상인 도서만 SELECT 합니다.
# 한 도서의 stock을 UPDATE 합니다.
# 한 도서를 DELETE 합니다.
# 각 단계의 결과를 pp()로 출력합니다.
# Python에서 psycopg를 사용합니다.
# SQL 값은 Parameter Binding 방식으로 전달합니다.