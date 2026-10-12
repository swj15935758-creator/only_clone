# day32_application.py
# 주제: 월간 예산 계획

import uuid
import psycopg
import streamlit as st

from day32_application_logic import calculate_budget
from day32_application_db import save_plan, list_plans, get_plan, summary


def main():
    st.set_page_config(
        page_title='월간 예산 계획',
        layout='wide'
    )

    st.title('월간 예산 계획')

    if 'preview_result' not in st.session_state:
        st.session_state.preview_result = None

    if 'request_key' not in st.session_state:
        st.session_state.request_key = None

    title = st.text_input(
        '계획 제목',
        max_chars=80
    )

    income = st.number_input(
        '수입',
        min_value=0,
        max_value=100000000,
        value=0,
        step=1
    )

    expense = st.number_input(
        '지출',
        min_value=0,
        max_value=100000000,
        value=0,
        step=1
    )

    preview_col, save_col = st.columns(2)
    preview_clicked = preview_col.button('계산 미리보기')
    save_clicked = save_col.button('DB 저장')

    if preview_clicked:
        try:
            clean_title = title.strip()

            if not clean_title or len(clean_title) > 80:
                raise ValueError(
                    '계획 제목은 1~80자로 입력하세요.'
                )

            result = calculate_budget(
                int(income),
                int(expense)
            )

            result['title'] = clean_title

            st.session_state.preview_result = result
            st.session_state.request_key = str(
                uuid.uuid4()
            )

        except ValueError as ve:
            st.warning(str(ve))

    preview_result = st.session_state.preview_result
    request_key = st.session_state.request_key

    if preview_result is not None:
        st.subheader('계산 미리보기')

        c1, c2, c3 = st.columns(3)

        c1.metric('수입',f'{preview_result["income"]:,}원')
        c2.metric('지출',f'{preview_result["expense"]:,}원')
        c3.metric('예상 잔액',f'{preview_result["balance"]:,}원')
        st.caption(f'요청 키: {request_key}')

    if save_clicked:
        if preview_result is None:
            st.warning('먼저 계산 미리보기를 실행하세요.')

        else:
            try:
                record_id = save_plan(
                    preview_result['title'],
                    preview_result,
                    request_key
                )

                if record_id is None:
                    st.info('같은 요청 키가 이미 저장되어 있습니다.')

                else:
                    st.success(f'저장 완료 ID: {record_id}')

            except ValueError as ve:
                st.warning(str(ve))

            except psycopg.Error as pe:
                st.error('DB 저장에 실패했습니다.')
                st.error(str(pe))

    st.subheader('전체 통계')

    try:
        stats = summary()
        stat1, stat2 = st.columns(2)
        stat1.metric('전체 계획 건수',stats['total_count'])
        stat2.metric('전체 잔액 합계',f'{stats["total_balance"]:,}원')

    except ValueError as ve:
        st.warning(str(ve))

    except psycopg.Error as pe:
        st.error('DB 조회에 실패했습니다.')
        st.error(str(pe))

    st.subheader('계획 목록')

    keyword = st.text_input('계획 제목 검색',max_chars=80)

    try:
        rows = list_plans(keyword)

        if rows:
            st.dataframe(
                rows,
                hide_index=True,
                width='stretch'
            )

        else:
            st.info('조회된 계획이 없습니다.')

    except ValueError as ve:
        st.warning(str(ve))

    except psycopg.Error as pe:
        st.error('DB 조회에 실패했습니다.')
        st.error(str(pe))

    st.subheader('ID별 상세 조회')

    record_id = st.number_input(
        '조회할 ID',
        min_value=1,
        value=1,
        step=1
    )

    if st.button('상세 조회'):
        try:
            record = get_plan(int(record_id))

            if record:
                st.write(record)
            else:
                st.info('해당 ID의 계획이 없습니다.')

        except ValueError as ve:
            st.warning(str(ve))

        except psycopg.Error as pe:
            st.error('DB 조회에 실패했습니다.')
            st.error(str(pe))


if __name__ == '__main__':
    main()