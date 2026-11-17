# day57_basic.py
# 채용 공고 제목 분류 API: 서버 추론 라우팅과 Pydantic 활용

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title='채용 공고 제목 분류 API')

# 요청 모델
class JobInput(BaseModel):
    title: str = Field(min_length=3, max_length=120)

# 응답 모델
class JobOutput(BaseModel):
    title: str
    category: str
    keyword_matched: bool

@app.post('/jobs/classify', response_model=JobOutput)
def classify_job(item: JobInput):
    title = item.title.strip()
    if '데이터' in title:
        category, matched = 'data', True
    elif '백엔드' in title:
        category, matched = 'backend', True
    else:
        category, matched = 'general', False
    return JobOutput(
        title=title,
        category=category,
        keyword_matched=matched
    )

