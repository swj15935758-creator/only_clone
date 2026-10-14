# day33_application.py
# 주제:
import re
from collections import Counter
from pathlib import Path
import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from util.print_util import pp
from include.graph_config import set_graph

jobs_dict = {
    "백엔드 개발": "python api 서버 데이터베이스 개발",
    "데이터 분석": "python pandas 통계 시각화 분석",
    "프론트엔드": "javascript react ui 화면 개발",
    "ML 엔지니어": "python 머신러닝 모델 배포 api"
}

# 공고명과 문서로 분류
job_titles = list(jobs_dict.keys())
job_texts = list(jobs_dict.values())

# 유사도 비교할 문서
search = ["python 모델 api"]

# 문서 전처리
def normalize(text):
    # 한글, 영문대소문자, 숫자, 공백문자가 아닌 것은 ' '로 변환
    text = re.sub(r'[^가-힣A-Za-z0-9\s]',' ',text)
    # 공백문자가 1개 이상이면 ' '로 변환 후 앞뒤 공백 제거후 소문자로 변환후 리턴
    return re.sub(r'\s+',' ',text).strip().lower()

# 문서 토큰화 코사인 유사도 비교 함수
def inspect_documents(documents):

    cleaned = [normalize(doc) for doc in documents] # 문서들 정규화한 리스트
    pp(cleaned)

    token_patten = r'(?u)\b\w+\b'

    vec = TfidfVectorizer(
        token_pattern=token_patten,
        norm='l2',
        smooth_idf=True
    )
    # TfidfVectorizer로 채용공고 4건을 벡터화
    job_matrix = vec.fit_transform(job_texts)

    # 코사인 유사도 비교할 문서 벡터화
    search_cleaned = [normalize(s) for s in search]
    search_matrix = vec.transform(search_cleaned)

    #  코사인 유사도 산출
    scores = cosine_similarity(search_matrix, job_matrix).flatten()
    scored_jobs = list(zip(job_titles, scores))
    scored_jobs.sort(key=lambda x: x[1], reverse=True)

    # 미등록 단어만 있는 질의는 점수 0으로 처리됨을 확인하세요.
    min_name, min_score = scored_jobs[-1]
    pp('미등록 단어만 있는 공고와 유사도 점수 :',min_name,min_score)

     # 가장 유사한 공고만 하나 출력
    pp(f'가장 유사한 공고: {scored_jobs[0][0]}')
    pp(f'가장 유사한 공고의 유사도: {scored_jobs[0][1]:.3f}')
inspect_documents(job_texts)