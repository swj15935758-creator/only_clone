# day32_basic.py
# 주제: 택배 배송 견적 계산 및 저장

import psycopg
import streamlit as st
from day32_basic_logic import calculate_shipping_quotes
from day32_basic_db import save_run, list_runs


def main():
    st.set_page_config(
        page_title='배송 견적 계산',
        layout='wide'
    )

    st.title('배송 견적 계산')

    with st.form('shipping_form'):
        label = st.text_input(
            '견적 제목',
            max_chars=80
        )

        weight = st.number_input(
            '무게(g)',
            min_value=1,
            max_value=20000,
            value=1,
            step=1
        )

        submitted = st.form_submit_button(
            '계산하고 저장'
        )

    if submitted:
        try:
            result = calculate_shipping_quotes(
                int(weight)
            )

            rid = save_run(
                label,
                result
            )

            left, right = st.columns(2)

            left.metric(
                '배송 요금',
                f'{result["fee"]:,}원'
            )

            right.metric(
                '저장 ID',
                rid
            )

            st.success('견적 저장 완료')

        except ValueError as ve:
            st.warning(str(ve))

        except psycopg.Error:
            st.error(
                'DB 연결에 실패했습니다.'
            )

    st.subheader('최신 견적 100건')

    try:
        rows = list_runs()

        if rows:
            st.dataframe(
                rows,
                hide_index=True,
                width='stretch'
            )

        else:
            st.info(
                '저장된 견적이 없습니다.'
            )

    except ValueError as ve:
        st.warning(str(ve))

    except psycopg.Error:
        st.error(
            'DB 연결에 실패했습니다.'
        )


if __name__ == '__main__':
    main()