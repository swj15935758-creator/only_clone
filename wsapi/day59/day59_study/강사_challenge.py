# day58_challenge.py
# 국제행사 다국어 더빙: 실제 Perso 프로젝트만 조회/생성

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from day58_ex import call, job_ids, PREFIX, file_url

app = FastAPI(title='국제 행사 영상 현지화')

# 번역 대상 언어 하나를 구조화 하는 JSON 구조 모델
class Target(BaseModel):
    languageCode: str # 번역 대상 언어 코드 (예: ko, ja, en ...)
    ttsModel: str | None = None

# 영상 더빙 프로젝트 생성에 필요한 요청 모델
class Campaign(BaseModel):
    spaceSeq: int = Field(gt=0)
    mediaSeq: int = Field(gt=0)
    title: str = Field(min_length=1)
    targetLanguages: list[Target] = Field(min_length=1)

# POST /campaigns/launch: 대상 언어 검증 > 큐 준비 > 실제 더빙 생성
@app.post('/campaigns/launch')
async def launch(data: Campaign, confirm_cost: bool = Query(False)):

    if not confirm_cost:
        raise HTTPException(400,'confirm_cost=true가 필요함')
    langs = await call('GET', PREFIX + '/languages') # 언어와 지원TTS모델들

    available = langs.get('result', langs).get('languages', []) # 지원 언어들

    for target in data.targetLanguages:
        if target.languageCode == 'auto':
            raise HTTPException(422, 'auto는 번역 대상이 아님')
        # 언어 목록에서 코드가 일치하는 항목들
        matches = [row for row in available if row.get('code')==target.languageCode]
        if not matches:
            raise HTTPException(422, '지원하지 않는 번역 언어')
        if target.ttsModel and \
            not any(target.ttsModel in row.get('supportedTtsModels', []) for row in matches):
            raise HTTPException(422, '지원하지 않는 언어/TTS 모델 조합')
    seq = data.spaceSeq
    await call('PUT', f'{PREFIX}/projects/spaces/{seq}/queue')
    payload = {
        'mediaSeq': data.mediaSeq,
        'isVideoProject': True,
        'sourceLanguageCode': 'auto',
        'targetLanguages': [t.model_dump(exclude_none=True) for t in data.targetLanguages],
        'preferredSpeedType': 'GREEN',
        'title': data.title
    }
    result = await call(
        'POST',
        f'{PREFIX}/projects/spaces/{seq}/translate',
        json=payload
    )
    return job_ids(result)

# GET /campaigns/{space_seq}/{project_seq}/status: 더빙 프로젝트 진행률 조회
@app.get('/campaigns/{space_seq}/{project_seq}/status')
async def status(space_seq: int, project_seq: int):
    return await call(
        'GET',
        f'{PREFIX}/projects/{project_seq}/space/{space_seq}/progress'
    )

# GET /campaigns/{space_seq}/{project_seq}/archive: 완료된 결과 아카이브 URL 조회
@app.get('/campaigns/{space_seq}/{project_seq}/archive')
async def archive(space_seq: int, project_seq: int):
    path = f'{PREFIX}/projects/{project_seq}'
    status_data = await call('GET', f'{path}/space/{space_seq}/progress')
    state = (status_data.get('result') or {}).get('progressReason') # 상태사유값
    if state != 'Completed': # 완료가 안되었다면
        raise HTTPException(409, f'작업이 완료되지 않음: {state}')
    result = await call(
        'GET',
        f'{path}/spaces/{space_seq}/download',
        params={'target': 'all'} # .tar 아카이브
    )
    info = result.get('result') or {}
    link = info.get('zippedFileDownloadLink')
    if not link:
        raise HTTPException(502, 'Perso 다운로드 링크가 없음')
    return {
        'projectSeq': project_seq,
        'url': file_url(link) # 상대경로 > 절대경로
    }
