# day33_application.py
# [Application: 채용공고 검색 엔진]
import re
from collections import Counter
from pathlib import Path
import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import soundfile as sf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from util.print_util import pp
from include.graph_config import set_graph
# 주제: 채용공고 텍스트 검색 (강의의 음성 처리 문서와 별도 주제)

# 채용공고:
# 백엔드 개발: "python api 서버 데이터베이스 개발"
# 데이터 분석: "python pandas 통계 시각화 분석"
# 프론트엔드: "javascript react ui 화면 개발"
# ML 엔지니어: "python 머신러닝 모델 배포 api"
jobs_dict = {
    "백엔드 개발": "python api 서버 데이터베이스 개발",
    "데이터 분석": "python pandas 통계 시각화 분석",
    "프론트엔드": "javascript react ui 화면 개발",
    "ML 엔지니어": "python 머신러닝 모델 배포 api"
}
job_titles = list(jobs_dict.keys())
job_texts = list(jobs_dict.values())

# 요구사항:
# 1) TfidfVectorizer로 채용공고 4건을 벡터화하세요.
# 정규화
def normalize(text):
    text = re.sub(r'[^가-힣A-Za-z0-9\s]', ' ', text)
    return re.sub(r'\s+',' ',text).strip().lower()

def vectorize_text(text):
    token_pattern = r'(?u)\b\w\w+\b'

    job_vec = TfidfVectorizer(
        token_pattern=token_pattern,
        norm='l2',
        smooth_idf=True
    )
    matrix = job_vec.fit_transform(text)
    return job_vec,matrix


# 2) 검색어 "python 모델 api"와 각 공고의 코사인 유사도를 산출하세요.
# 유사도 구하는 함수
def cosine_same_rate(job_vec, matrix, text):
    text = normalize(text)
    text_vector = job_vec.transform([text])
    scores = cosine_similarity(text_vector,matrix)[0]

    return scores

# 3) 점수 내림차순으로 공고명·점수를 출력하세요.
# 내림차순 공고명 점수 출력하는 함수
def print_name_scores(job_titles, scores):
    scores_dict = {}

    for job_title, score in zip(job_titles, scores):
        scores_dict[job_title] = score

    sorted_scores = sorted(
        scores_dict.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for job_title, score in sorted_scores:
        pp(f'{job_title}: {score:.3f}')

    return sorted_scores
# 4) 미등록 단어만 있는 질의는 점수 0으로 처리됨을 확인하세요.
def check_unknown_txt(job_vec, matrix):
    unknown_txt = '요리 여행 음악'

    unknown_scores = cosine_same_rate(
        job_vec,
        matrix,
        unknown_txt
    )

    pp('미등록 단어 질의 점수:',np.round(unknown_scores, 3))
    return unknown_scores

# 5) 가장 유사한 공고 하나를 출력하세요.
def print_best_job(sorted_scores):
    best_title, best_score = sorted_scores[0]

    pp(
        f'가장 유사한 공고: {best_title}, '
        f'점수: {best_score:.3f}'
    )
    return best_title, best_score

if __name__ == '__main__':
    job_vec, matrix = vectorize_text(job_texts)
    scores = cosine_same_rate(job_vec,matrix,'python 모델 api')
    sorted_scores = print_name_scores(job_titles,scores)