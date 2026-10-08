import pandas as pd

from day30_challenge_db import(
    has_database_url,
    create_table,
    save_model_experiment,
    load_model_experiments,
    delete_model_experiment,
)

def has_database_url_logic():
    return has_database_url()

def create_table_logic():
    return create_table()

def validate_model_experiment(
    model_name,
    dataset_name,
    accuracy
):
    if not model_name.strip():
        return '모델명을 입력하세요.'

    if not dataset_name.strip():
        return '데이터셋명을 입력하세요.'

    if accuracy < 0.0 or accuracy > 1.0:
        return '정확도는 0.0에서 1.0 사이여야 합니다.'

    return None

def register_model_experiment(
    model_name,
    dataset_name,
    accuracy,
    memo
):
    return save_model_experiment(
        model_name,
        dataset_name,
        accuracy,
        memo
    )

def search_model_experiments(min_accuracy):
    rows = load_model_experiments(min_accuracy)

    return pd.DataFrame(
        rows,
        columns=[
            'id',
            'model_name',
            'dataset_name',
            'accuracy',
            'memo',
            'created_at'
        ]
    )

def remove_model_experiment(experiment_id):
    return delete_model_experiment(experiment_id)
