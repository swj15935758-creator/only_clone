import psycopg
import streamlit as st

from day30_application_logic import(
    has_database_url_logic,
    create_table_logic,
    STATUSES,
    validate_job_application,
    register_job_application,
    search_job_applications,
    modify_job_application_status,
)

def show_insert_form():
    st.subheader('채용 공고 지원 등록')

    with st.form(
        'job_application_form',
        clear_on_submit=True
    ):
        company = st.text_input(
            '회사명',
            placeholder='예: 네이버'
        )

        position = st.text_input(
            '지원 직무',
            placeholder='예: 백엔드 개발자'
        )

        status = st.selectbox(
            '상태',
            STATUSES
        )

        memo = st.text_area(
            '메모',
            placeholder='지원 관련 메모를 입력하세요.'
        )

        submitted = st.form_submit_button('저장')

    if not submitted:
        return

    error_message = validate_job_application(
        company,
        position
    )

    if error_message:
        st.warning(error_message)
        return

    try:
        new_id = register_job_application(
            company,
            position,
            status,
            memo
        )

        st.success(
            f'지원 정보를 저장했습니다. ID: {new_id}'
        )

    except psycopg.Error:
        st.error(
            '데이터베이스 저장 중 문제가 발생했습니다.'
        )

def show_search_list():
    st.subheader('채용 공고 지원 조회')

    keyword = st.text_input(
        '회사명 검색',
        placeholder='회사명의 일부를 입력하세요.'
    )

    try:
        df = search_job_applications(keyword)

        st.dataframe(
            df,
            hide_index=True,
            width='stretch'
        )

    except psycopg.Error:
        st.error(
            '데이터베이스 조회 중 문제가 발생했습니다.'
        )

def show_update_status():
    st.subheader('지원 상태 수정')

    application_id = st.number_input(
        '대상 ID',
        min_value=1,
        step=1
    )

    status = st.selectbox(
        '변경할 상태',
        STATUSES,
        key='update_status'
    )

    if st.button(
        '상태 수정',
        type='primary',
        width='stretch'
    ):
        try:
            count = modify_job_application_status(
                application_id,
                status
            )

            if count:
                st.success('지원 상태를 수정했습니다.')
            else:
                st.warning('해당 ID가 없습니다.')

        except psycopg.Error:
            st.error(
                '데이터베이스 수정 중 문제가 발생했습니다.'
            )

def main():
    st.set_page_config(
        page_title='채용 공고 지원 관리',
        page_icon='💼',
        layout='wide'
    )

    st.title('채용 공고 지원 관리')

    if not has_database_url_logic():
        st.error(
            'DATABASE_URL 환경변수를 설정하세요.'
        )
        st.stop()

    try:
        create_table_logic()

    except psycopg.Error:
        st.error(
            'PostgreSQL 연결 또는 테이블 생성에 실패했습니다.'
        )
        st.stop()

    tab1, tab2, tab3 = st.tabs([
        '등록',
        '조회',
        '상태 수정'
    ])

    with tab1:
        show_insert_form()

    with tab2:
        show_search_list()

    with tab3:
        show_update_status()

if __name__ == '__main__':
    main()
