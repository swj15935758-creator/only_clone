# day55_application.py
# 주제: Application | 채용 공고 검색 API 취업 공고 등록과 기술 스택 필터링

from typing import Literal
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title='application',
    description='FastAPI application 입니다.',
    version='0.0.1'
)

class JobPost(BaseModel):
    company: str = Field(min_length=2, max_length=50)
    position: str = Field(min_length=2, max_length=60)
    level: Literal['junior', 'mid']
    skills: list[str] = Field(min_length=1, max_length=8)
    salary_min: int = Field(ge=0)

class JobOut(JobPost):
    id: int

posts: dict[int, dict] = {}
next_post_id = 1

@app.post('/posts', response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(job: JobPost):
    global next_post_id

    payload = job.model_dump()
    payload['id'] = next_post_id
    posts[next_post_id] = payload
    next_post_id += 1

    return payload

@app.get('/posts', response_model=list[JobOut])
def list_jobs(
    skill: str | None = Query(default=None, min_length=1),
    min_salary: int | None = Query(default=None, ge=0)
):
    results = []

    for post in posts.values():
        if skill is not None:
            saved_skills = [item.lower() for item in post['skills']]
            if skill.lower() not in saved_skills:
                continue

        if min_salary is not None and post['salary_min'] < min_salary:
            continue

        results.append(post)

    return results

@app.get('/posts/{post_id}', response_model=JobOut)
def get_job(post_id: int = Path(ge=1)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail='공고를 찾을 수 없습니다.')

    return posts[post_id]

@app.delete('/posts/{post_id}')
def delete_job(post_id: int = Path(ge=1)):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail='공고를 찾을 수 없습니다.')

    del posts[post_id]
    return {'id': post_id, 'message': '공고 삭제 완료'}