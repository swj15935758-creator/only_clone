import psycopg
import streamlit as st

from day30_basic_logic import(
    has_database_url_logic,
    create_table_logic,
    validate_study_schedule,
    register_study_schedule,
    search_study_schedule,
)

def show_insert_form():
    st.subheader('스터디 일정 등록')

    with st.form('study_schedule_form',clear_on_submit=True):
        subject = st.text_input('학습 주제',placeholder='예: PostgreSQL 공부')
        study_date = st.date_input('학습 날짜',value=None)
        place = st.text_input('장소',placeholder='예: 도서관')
        submitted = st.form_submit_button('저장')

    if not submitted:
        return

    error_message = validate_study_schedule(
        subject,
        study_date,
        place
    )

    if error_message:
        st.warning(error_message)
        return

    try:
        new_id = register_study_schedule(
            subject,
            study_date,
            place
        )

        st.success(f'일정을 저장했습니다. ID: {new_id}')

    except psycopg.Error:
        st.error('데이터베이스 저장 중 문제가 발생했습니다.')


def show_study_schedule():
    st.subheader('스터디 일정 조회')

    try:
        df = search_study_schedule()

        st.dataframe(
            df,
            hide_index=True,
            width='stretch'
        )

    except psycopg.Error:
        st.error('데이터베이스 조회 중 문제가 발생했습니다.')


def main():
    st.set_page_config(
        page_title='스터디 일정 관리',
        page_icon='📚',
        layout='wide'
    )

    st.title('스터디 일정 관리')

    if not has_database_url_logic():
        st.error('DATABASE_URL 환경변수를 설정하세요.')
        st.stop()

    try:
        create_table_logic()

    except psycopg.Error:
        st.error('PostgreSQL 연결 또는 테이블 생성에 실패했습니다.')
        st.stop()

    tab1, tab2 = st.tabs(['일정 등록','일정 조회'])

    with tab1:
        show_insert_form()

    with tab2:
        show_study_schedule()


if __name__ == '__main__':
    main()