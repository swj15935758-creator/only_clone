# challenge.py

import psycopg
from db import get_connection, load_sql
from util.print_util import pp


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql('challenge_create_table.sql'))


def add_run(conn, model_name, dataset_name, accuracy, epochs, memo):
    with conn.cursor() as cur:
        cur.execute(
            load_sql('challenge_add_run.sql'),
            (model_name, dataset_name, accuracy, epochs, memo)
        )

        return cur.fetchone()[0] # 등록 후 등록된 자동 증가 번호 리턴


def get_runs(conn):
    with conn.cursor() as cur:
        cur.execute(load_sql('challenge_get_runs.sql'))

        return cur.fetchall()


def get_runs_by_accuracy(conn, min_accuracy):
    with conn.cursor() as cur:
        cur.execute(
            load_sql('challenge_get_runs_by_accuracy.sql'),
            (min_accuracy,)
        )

        return cur.fetchall()


def update_memo(conn, run_id, memo):
    with conn.cursor() as cur:
        cur.execute(
            load_sql('challenge_update_memo.sql'),
            (memo, run_id)
        )

        return cur.rowcount


def delete_run(conn, run_id):
    with conn.cursor() as cur:
        cur.execute(
            load_sql('challenge_delete_run.sql'),
            (run_id,)
        )

        return cur.rowcount


def main():
    try:

        with get_connection() as conn:
            create_table(conn)

            with conn.cursor() as cur:
                cur.execute(load_sql('challenge_trunct_run.sql'))

            conn.commit()
            pp('정상')

            try:
                id1 = add_run(
                    conn,
                    'CNN',
                    'FashionMNIST',
                    0.9125,
                    15,
                    '기본모델'
                )

                id2 = add_run(
                    conn,
                    'MLP',
                    'FashionMNIST',
                    0.8870,
                    20,
                    'DENSE 모델'
                )

                pp(f'생성 id {id1}, id {id2}')

                updated = update_memo(
                    conn,
                    id1,
                    '튜닝예정'
                )

                pp(f'수정 row 수:{updated}')

                conn.commit()

            except Exception as e:
                conn.rollback()

                pp(f'Transaction 취소 {e}')


            pp(get_runs(conn))

            pp('정확도 0.90 이상')
            pp(get_runs_by_accuracy(conn, 0.90))


            pp('의도적인 오류와 ROLLBACK')

            try:
                add_run(
                    conn,
                    None,
                    'Iris',
                    0.9125,
                    20,
                    '오류실험'
                )

                conn.commit()

            except Exception as e:
                conn.rollback()

                pp(f'ROLLBACK {e}')


            pp('ROLLBACK 이후 데이터')
            pp(get_runs(conn))


            pp('삭제')

            pp(
                f'삭제 row 수 : {delete_run(conn, id2)}'
            )

            conn.commit()

            pp(get_runs(conn))


    except psycopg.Error as e:
        pp(f'Error: {e}')


if __name__ == '__main__':
    main()