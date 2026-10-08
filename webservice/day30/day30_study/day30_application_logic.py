import pandas as pd

from day30_application_db import(
    has_database_url,
    create_table,
    save_job_application,
    load_job_applications,
    update_job_application_status,
)

STATUSES = ['관심', '지원', '면접', '결과']

def has_database_url_logic():
    return has_database_url()

def create_table_logic():
    return create_table()

def validate_job_application(company, position):
    if not company.strip():
        return '회사명을 입력하세요.'

    if not position.strip():
        return '지원 직무를 입력하세요.'

    return None

def register_job_application(company, position, status, memo):
    return save_job_application(
        company,
        position,
        status,
        memo
    )

def search_job_applications(keyword=''):
    rows = load_job_applications(keyword)

    return pd.DataFrame(
        rows,
        columns=[
            'id',
            'company',
            'position',
            'status',
            'memo'
        ]
    )

def modify_job_application_status(application_id, status):
    return update_job_application_status(
        application_id,
        status
    )
