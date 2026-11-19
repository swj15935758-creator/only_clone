# day58_application.py
# 팟캐스트 STT: 실제 Perso의 업로드된 mediaSeq를 녹취

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from ..day59_ex import call, job_ids, PREFIX

app = FastAPI(title='팟캐스트 STT 아카이브')

# 요청 모델 클래스
class Episode(BaseModel):
    spaceSeq: int = Field(gt=0)
    mediaSeq: int = Field(gt=0)
    title: str = Field(min_length=1)

# POST /episode/transcribe: 작업 큐 준비 후 실제 STT 프로젝트 생성
@app.get('/episode/transcribe')
async def transcribe(data: Episode, confirm_cost: bool = Query(False)):
    if not confirm_cost:
        raise HTTPException(400, 'confirm_cost=true가 필요함')
    seq = data.spaceSeq
    # Perso 작업 큐 초기화 또는 기존 큐 상태 확인
    await call('PUT', f'{PREFIX}/projects/spaces/{seq}/queue')
    # 실제 생성 호출: mediaSeq에 등록된 음성을 텍스트로 변환하는 STT 작업
    result = await call(
        'POST',
        f'{PREFIX}/projects/spaces/{seq}/stt',
        json={
            'mediaSeq': data.mediaSeq,
            'isVideoProject': False,
            'title': data.title
        }
    )
    return job_ids(result)

# GET /episodes/{space_seq}/{project_seq}/status: STT 생성 진행 상태를 한 번 조회
@app.get('/episodes/{space_seq}/{project_seq}/status')
async def status(space_seq: int, project_seq: int):
    return await call('GET', f'{PREFIX}/projects/{project_seq}/spaces/{space_seq}/progress')

# GET /episodes/{space_seq}/{project_seq}/script: 생성된 STT 문장, 화자, 시각 조회
@app.get('/episodes/{space_seq}/{project_seq}/script')
async def script(space_seq: int, project_seq: int, cursor_id: int|None = None):
    params = {'size': 100} # 한 번에 최대 100개 문장을 요청
    if cursor_id is not None:
        params['cursor_id'] = cursor_id
    return await call(
        'GET',
        f'{PREFIX}/projects/{project_seq}/spaces/{space_seq}/stt/script',
        params=params
    )



