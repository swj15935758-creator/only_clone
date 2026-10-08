# day29_challenge.py
# 주제:Challenge 과제 - AI 모델 실험 이력 관리

from db import get_connection, load_sql
from util.print_util import pp

# 주제
# 머신러닝 모델의 실험 결과를 PostgreSQL에 안전하게 저장하고
# Transaction과 예외처리를 적용합니다.

# 테이블명
# model_runs

# 필수 컬럼
# id: 자동 증가 Primary Key
# model_name: 모델명
# dataset_name: 데이터셋명
# accuracy: 정확도
# epochs: 학습 횟수
# memo: 메모


def create_model_runs_table(conn):
    sql = load_sql('create_model_runs_table.sql')

    with conn.cursor() as cur:
        cur.execute(sql)

    conn.commit()


def insert_model_run(conn,model_name,dataset_name,accuracy,epochs,memo):
    sql = load_sql('insert_model_run.sql')

    with conn.cursor() as cur:
        cur.execute(
            sql,
            (model_name,dataset_name,accuracy,epochs,memo))

        model_run_id = cur.fetchone()[0]
    return model_run_id


def select_model_runs(conn):
    sql = load_sql('select_model_runs.sql')

    with conn.cursor() as cur:
        cur.execute(sql)

        rows = cur.fetchall()

    return rows


def select_model_runs_by_accuracy(conn, min_accuracy):
    sql = load_sql('select_model_runs_by_accuracy.sql')

    with conn.cursor() as cur:
        cur.execute(
            sql,
            (min_accuracy,)
        )

        rows = cur.fetchall()

    return rows


def update_model_run_accuracy(conn, model_run_id, accuracy):
    sql = load_sql('update_model_run_accuracy.sql')

    with conn.cursor() as cur:
        cur.execute(
            sql,
            (accuracy, model_run_id)
        )

        row_count = cur.rowcount

    return row_count


def delete_model_run(conn, model_run_id):
    sql = load_sql('delete_model_run.sql')

    with conn.cursor() as cur:
        cur.execute(
            sql,
            (model_run_id,)
        )

        row_count = cur.rowcount

    return row_count


def success_transaction(conn):
    try:
        model_run_id = insert_model_run(conn,'CNN','MNIST',0.95,20,'CNN 실험')
        pp(model_run_id)
        row_count = update_model_run_accuracy(conn,model_run_id,0.97)
        pp(row_count)
        conn.commit()
        pp('Transaction COMMIT 완료')

    except Exception as e:
        conn.rollback()
        pp('Transaction ROLLBACK')
        pp(e)


def fail_transaction(conn):
    try:
        model_run_id = insert_model_run(
            conn,
            'LSTM',
            'Sensor',
            0.91,
            30,
            '정상 데이터'
        )

        pp(model_run_id)

        insert_model_run(
            conn,
            'GRU',
            'Sensor',
            1.5,
            20,
            '잘못된 accuracy'
        )

        conn.commit()

        pp('Transaction COMMIT 완료')

    except Exception as e:
        conn.rollback()

        pp('잘못된 입력으로 ROLLBACK 실행')
        pp(e)


def main():
    conn = get_connection()

    try:
        create_model_runs_table(conn)

        model_run_id1 = insert_model_run(
            conn,
            'RandomForest',
            'Customer Churn',
            0.89,
            10,
            '기본 실험'
        )

        conn.commit()

        pp(model_run_id1)

        model_run_id2 = insert_model_run(
            conn,
            'CNN',
            'MNIST',
            0.94,
            20,
            '이미지 분류'
        )

        conn.commit()

        pp(model_run_id2)

        model_run_id3 = insert_model_run(
            conn,
            'LSTM',
            'Sensor',
            0.92,
            30,
            '시계열 분류'
        )

        conn.commit()

        pp(model_run_id3)

        pp(select_model_runs(conn))

        pp(select_model_runs_by_accuracy(conn,0.90))

        row_count = update_model_run_accuracy(conn,model_run_id1,0.93)
        conn.commit()
        pp(row_count)

        row_count = delete_model_run(conn,model_run_id2)

        conn.commit()
        pp(row_count)
        success_transaction(conn)
        fail_transaction(conn)
        pp(select_model_runs(conn))

    finally:
        conn.close()


if __name__ == '__main__':
    main()


    