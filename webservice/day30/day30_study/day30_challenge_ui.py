import psycopg
import streamlit as st

from day30_challenge_logic import(
    has_database_url_logic,
    create_table_logic,
    validate_model_experiment,
    register_model_experiment,
    search_model_experiments,
    remove_model_experiment,
)

def show_insert_form():
    st.subheader('AI 모델 실험 등록')

    with st.form(
        'model_experiment_form',
        clear_on_submit=True
    ):
        model_name = st.text_input(
            '모델명',
            placeholder='예: RandomForest'
        )

        dataset_name = st.text_input(
            '데이터셋명',
            placeholder='예: churn.csv'
        )

        accuracy = st.number_input(
            '정확도',
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01,
            format='%.2f'
        )

        memo = st.text_area(
            '메모',
            placeholder='실험 내용을 입력하세요.'
        )

        submitted = st.form_submit_button('저장')

    if not submitted:
        return

    error_message = validate_model_experiment(
        model_name,
        dataset_name,
        accuracy
    )

    if error_message:
        st.warning(error_message)
        return

    try:
        new_id = register_model_experiment(
            model_name,
            dataset_name,
            accuracy,
            memo
        )

        st.success(
            f'실험 기록을 저장했습니다. ID: {new_id}'
        )

    except psycopg.Error:
        st.error(
            '데이터베이스 저장 중 문제가 발생했습니다.'
        )

def show_experiment_list():
    st.subheader('AI 모델 실험 조회')

    min_accuracy = st.number_input(
        '최소 정확도',
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01,
        format='%.2f'
    )

    try:
        df = search_model_experiments(min_accuracy)

        st.dataframe(
            df,
            hide_index=True,
            width='stretch'
        )

    except psycopg.Error:
        st.error(
            '데이터베이스 조회 중 문제가 발생했습니다.'
        )

def show_delete_experiment():
    st.subheader('AI 모델 실험 삭제')

    experiment_id = st.number_input(
        '삭제할 ID',
        min_value=1,
        step=1
    )

    confirmed = st.checkbox(
        '삭제할 내용을 확인했습니다.'
    )

    if st.button(
        '삭제',
        type='primary',
        width='stretch'
    ):
        if not confirmed:
            st.warning(
                '삭제 전 확인 Checkbox를 선택하세요.'
            )
            return

        try:
            count = remove_model_experiment(
                experiment_id
            )

            if count:
                st.success('실험 기록을 삭제했습니다.')
            else:
                st.warning('해당 ID가 없습니다.')

        except psycopg.Error:
            st.error(
                '데이터베이스 삭제 중 문제가 발생했습니다.'
            )

def main():
    st.set_page_config(
        page_title='AI 모델 실험 기록 관리',
        page_icon='🤖',
        layout='wide'
    )

    st.title('AI 모델 실험 기록 관리')

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
        '삭제'
    ])

    with tab1:
        show_insert_form()

    with tab2:
        show_experiment_list()

    with tab3:
        show_delete_experiment()

if __name__ == '__main__':
    main()
