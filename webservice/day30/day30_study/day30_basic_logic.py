import pandas as pd

from day30_basic_db import(
    has_database_url,
    create_table,
    save_study_schedule,
    load_study_schedule,
)

def has_database_url_logic():
    return has_database_url()

def create_table_logic():
    return create_table()

def validate_study_schedule(subject, study_date, place):
    if not subject.strip():
        return '학습 주제를 입력하세요.'

    if study_date is None:
        return '학습 날짜를 선택하세요.'

    if not place.strip():
        return '장소를 입력하세요.'

    return None

def register_study_schedule(subject, study_date, place):
    return save_study_schedule(
        subject,
        study_date,
        place
    )

def search_study_schedule():
    rows = load_study_schedule()

    return pd.DataFrame(
        rows,
        columns=[
            'id',
            'subject',
            'study_date',
            'place'
        ]
    )