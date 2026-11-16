# day57_basic.py
# 주제: Basic: 채용 공고 키워드 분류 API
# 실습의 캠퍼스 의도 분류와 다른 주제인 '채용 공고 분석'을 구현하세요.

from fastapi import FastAPI
from pydantic import BaseModel, Field

# [요구사항
# POST /jobs/classify JSON 입력: title (3~120자).
# title에 '데이터' 포함 → data, '백엔드' 포함 → backend, 그 외 → general.
# 응답: title, category, keyword_matched.
# 빈 문자열과 2글자 제목은 HTTP 422여야 합니다.
# /docs에서 3가지 정상 케이스와 1가지 오류 케이스를 점검하세요.]

app = FastAPI(title='채용 공고 키워드 분류 API')

class Job(BaseModel):
    title: str = Field(min_length=3, max_length=120)

class JobResponse(BaseModel):
    title: str
    category: str
    keyword_matched: str | None

@app.post('/jobs/classify', response_model=JobResponse)
def classify_job(request: Job):
    if '데이터' in request.title:
        category = 'data'
        keyword_matched = '데이터'
    elif '백엔드' in request.title:
        category = 'backend'
        keyword_matched = '백엔드'
    else:
        category = 'general'
        keyword_matched = None

    return JobResponse(
        title=request.title,
        category=category,
        keyword_matched=keyword_matched
    )