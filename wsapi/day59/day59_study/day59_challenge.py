# day59_challenge.py
# 주제:[Challenge] 국제행사 홍보영상 다국어 더빙 실서비스

import os
from urllib.parse import quote, urlsplit, urlunsplit
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from pydantic import BaseModel, Field

# 기본 설정
load_dotenv() # .env 읽음
BASE = 'https://api.perso.ai'  # Perso API 서버
MEDIA = 'https://portal-media.perso.ai'  # 결과 파일 서버
PREFIX = '/video-translator/api/v1'
KEY = os.getenv('PERSO_API_KEY', '').strip()
SPACE_SEQ = 612722  # 기본 작업 공간: 실제 조회한 Space로 변경 가능
MAX_UPLOAD = 25 * 1024 * 1024  # 교육용 업로드 제한: 25MB

# app 모듈 생성
app = FastAPI(title='[Challenge] 국제행사 홍보영상 다국어 더빙 실서비스')
# 원래 함수나 클래스는 import 해서 가져오지만 여기서는 생략
# 함수====================
# 비동기 클라이언트 생성 함수
def make_client(timeout: float = 60.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=timeout, follow_redirects=False)
# json 문자열로 안전하게 처리 함수
def parse_response(response: httpx.Response) -> dict:
    try:
        data = response.json() if response.content else {}
    except ValueError:
        data = {'message': response.text[:120]}
    if response.status_code >= 400:
        err = data if isinstance(data, dict) else {'message': str(data)}
        raise HTTPException(
            status_code=response.status_code,
            detail={
                'code': err.get('code', ''),
                'detailCode': err.get('detailCode', ''),
                'message': err.get('message', err.get('detail',
                                                    '외부 API 오류')),
            },
        )
    if not isinstance(data, dict):
        raise HTTPException(502, '예상하지 못한 Perso 응답 형식')
    return data
# 비동기로 요청을 보내는 함수
async def call(method: str, path: str, *, params=None, json=None) -> dict:
    if not KEY:
        raise HTTPException(503, 'PERSO_API_KEY 환경 변수가 없습니다')
    try:
        async with make_client() as client:
            response = await client.request(
                method, BASE + path, params=params, json=json,
                headers={'XP-API-KEY': KEY},
            )
    except httpx.TimeoutException as exc:
        raise HTTPException(504, 'Perso API 요청 시간 초과') from exc
    except httpx.RequestError as exc:
        raise HTTPException(502, 'Perso API 연결 오류') from exc
    return parse_response(response)
# 응답 다운로트 경로 URL 로 반환 함수
def file_url(path: str) -> str:
    if not isinstance(path, str) or not path.startswith('/'):
        raise HTTPException(502, '미디어 경로가 올바르지 않습니다')
    if path.startswith('//') or '\\' in path or '\x00' in path:
        raise HTTPException(502, '허용되지 않은 미디어 경로')
    return MEDIA + quote(path, safe='/%')
# ProjectSeq 추출 함수
def job_ids(data: dict) -> dict:
    result = data.get('result') or {}
    ids = result.get('startGenerateProjectIdList', [])
    if not isinstance(ids, list) or not ids:
        raise HTTPException(502, 'Perso 응답에 프로젝트 ID가 없습니다')
    return {'projectSeqList': ids,
            'message': '프로젝트별 진행률을 별도로 확인하세요'}
# 생성 작업 비동기 공통 함수
async def create_job(space_seq: int, kind: str, body: dict,confirm: bool) -> dict:
    if not confirm:
        raise HTTPException(400, '생성에는 confirm_cost=true가 필요합니다')
    result = await call(
        'POST',
        f'{PREFIX}/projects/spaces/{space_seq}/{kind}'
        ,json=body
    )
    return job_ids(result)

# Pydantic 요청 모델: 미디어의 길이·용량·해상도 등 메타데이터 검증
class MediaMeta(BaseModel):
    spaceSeq: int = Field(gt=0)
    durationMs: int = Field(gt=0)
    originalName: str = Field(min_length=1)
    mediaType: str = Field(pattern='^(audio|video)$')
    extension: str = Field(min_length=2)
    size: int = Field(ge=0)
    width: int | None = None
    height: int | None = None
    sttMode: bool = False
# STT/오디오 분리 생성에 사용할 공통 요청 모델
class CreateJob(BaseModel):
    mediaSeq: int = Field(gt=0)
    isVideoProject: bool = False
    title: str = 'Perso 실습'
# 번역 언어와 해당 언어의 TTS 모델 선택
class TargetLanguage(BaseModel):
    languageCode: str = Field(min_length=2)
    ttsModel: str | None = None
# Dubbing 요청 모델: 원본 언어, 목표 언어, 화자 수, 처리 옵션
class TranslateJob(CreateJob):
    sourceLanguageCode: str = 'auto'
    targetLanguages: list[TargetLanguage] = Field(min_length=1)
    numberOfSpeakers: int = Field(default=1, ge=1)
    withLipSync: bool = False
    preferredSpeedType: str = Field(default='GREEN',pattern='^(GREEN|RED)$')
# Lip Sync 요청 모델: 속도와 새 프로젝트 제목
class LipSyncJob(BaseModel):
    preferredSpeedType: str = Field(default='GREEN',
                                    pattern='^(GREEN|RED)$')
    title: str = '립싱크 생성'

# 업로드 파일명에서 경로 제거 및 빈 이름 거부
def clean_name(filename: str | None) -> str:
    name = (filename or '').replace('\\', '/').split('/')[-1]
    if not name or name in ('.', '..'):
        raise HTTPException(422, '올바른 파일명이 필요합니다')
    return name
# 최대 25MB까지만 메모리로 읽어 업로드 초과를 감지
async def read_upload(file: UploadFile) -> bytes:
    raw = await file.read(MAX_UPLOAD + 1)
    if not raw:
        raise HTTPException(422, '빈 파일은 업로드할 수 없습니다')
    if len(raw) > MAX_UPLOAD:
        raise HTTPException(413, '업로드 파일은 최대 25MB입니다')
    return raw
# Perso에서 발급한 SAS URL의 안전성을 검사하는 함수
def check_sas_url(sas_url: str) -> None:
    # SAS URL을 구성 요소별로 분리
    parsed = urlsplit(sas_url)
    # URL의 호스트 이름 추출
    host = (parsed.hostname or '').lower()
    # 실제 Perso API에서 확인된 호스트를 허용 목록에 추가
    allowed = (
        host == 'perso-studio-file.perso.ai'
        or host == 'perso-saas-file-frontdoor.perso.ai'
        or host.endswith('.blob.core.windows.net')
    )
    # HTTPS가 아니면 업로드 차단
    if parsed.scheme != 'https':
        raise HTTPException(502, 'SAS URL은 HTTPS여야 합니다')
    # 허용된 호스트가 아니면 업로드 차단
    if not allowed:
        raise HTTPException(
            502,
            f'허용되지 않은 SAS 호스트: {host}'
        )
    # SAS 서명 Query가 없으면 업로드 차단
    if not parsed.query:
        raise HTTPException(502, 'SAS 서명 Query가 없습니다')
    # URL에 사용자 이름, 암호, 별도 포트가 있으면 차단
    if parsed.username or parsed.password or parsed.port:
        raise HTTPException(502, 'SAS URL 호스트 정보가 잘못되었습니다')
# 업로드 1단계: Perso에서 30분 유효한 blobSasUrl 발급
async def request_sas(file_name: str) -> str:
    data = await call('GET', '/file/api/upload/sas-token',
                      params={'fileName': file_name})
    sas_url = data.get('blobSasUrl')
    if not isinstance(sas_url, str):
        raise HTTPException(502, 'Perso 응답에 blobSasUrl이 없습니다')
    check_sas_url(sas_url)
    return sas_url
# 업로드 2단계: SAS가 가진 인증권한으로 Azure에 파일 바이너리 PUT
async def put_blob(sas_url: str, raw: bytes) -> int:
    check_sas_url(sas_url)
    try:
        async with make_client(120.0) as client:
            response = await client.put(
                sas_url, content=raw,
                headers={'x-ms-blob-type': 'BlockBlob',
                         'Content-Type': 'application/octet-stream'},
            )
    except httpx.TimeoutException as exc:
        raise HTTPException(504, 'Azure 업로드 시간 초과') from exc
    except httpx.RequestError as exc:
        raise HTTPException(502, 'Azure 업로드 연결 오류') from exc
    if response.status_code != 201:
        raise HTTPException(502,
                            f'Azure 업로드 실패: HTTP {response.status_code}')
    return response.status_code
# 업로드 3단계: 등록 요청으로 실제 mediaSeq 취득
async def register_media(space_seq: int, kind: str, sas_url: str,file_name: str) -> int:
    check_sas_url(sas_url)
    if kind not in ('audio', 'video'):
        raise HTTPException(422, 'kind는 audio 또는 video')
    parts = urlsplit(sas_url)
    stable_url = urlunsplit((parts.scheme, parts.netloc, parts.path, '', ''))
    data = await call('PUT', f'/file/api/upload/{kind}', json={
        'spaceSeq': space_seq, 'fileUrl': stable_url,
        'fileName': file_name,
    })
    media_seq = data.get('seq')
    if not isinstance(media_seq, int):
        raise HTTPException(502, 'Perso 응답에 mediaSeq가 없습니다')
    return media_seq

# 요구사항
# 1. 본인이 제작하거나 사용 권한이 있는 홍보 영상을 업로드하여 mediaSeq를 받습니다.
@app.post('/perso/upload')
async def perso_upload(
        file: UploadFile = File(...),
        kind: str = Query('audio', pattern='^(audio|video)$'),
        space_seq: int = Query(SPACE_SEQ, ge=0),
):
    try:
        file_name = clean_name(file.filename)
        raw = await read_upload(file)
    finally:
        await file.close()
    sas_url = await request_sas(file_name)
    azure_status = await put_blob(sas_url, raw)
    media_seq = await register_media(space_seq, kind, sas_url, file_name)

    return {
        'mediaSeq': media_seq,
        'spaceSeq': space_seq,
        'kind': kind,
        'fileName': file_name,
        'size': len(raw),
        'azureHttpStatus': azure_status,
        'message': 'Perso 파일 등록 완료'
    }

# 2. 실제 Language API의 언어/TTS 조합을 확인합니다.
@app.get('/perso/languages')
async def perso_languages():
    return await call('GET', f'{PREFIX}/languages')


# 3. /campaigns/launch?confirm_cost=true로 2개 언어의 더빙을 요청합니다.
@app.post('/campaigns/launch')
async def perso_campaigns_dubbing(
    body: TranslateJob,
    space_seq: int = Query(..., gt=0),
    confirm_cost: bool = Query(False),
):
    if len(body.targetLanguages) != 2:
        raise HTTPException(422, '대상 언어를 2개 입력하세요')

    if len({target.languageCode for target in body.targetLanguages}) != 2:
        raise HTTPException(422, '서로 다른 대상 언어 2개를 입력하세요')

    if any(target.languageCode == 'auto' for target in body.targetLanguages):
        raise HTTPException(422, 'auto를 대상 언어로 사용할 수 없습니다')

    if not body.isVideoProject:
        raise HTTPException(422, '홍보 영상은 isVideoProject=true로 입력하세요')

    return await create_job(
        space_seq,
        'translate',
        body.model_dump(exclude_none=True),
        confirm_cost,
    )


# 4. 발급된 각 projectSeq를 독립적으로 상태 조회합니다.
@app.get('/campaigns/{project_seq}/status')
async def campaign_status(
    project_seq: int,
    space_seq: int = Query(..., gt=0),
):
    project = await call(
        'GET',
        f'{PREFIX}/projects/{project_seq}/spaces/{space_seq}',
    )

    return {
        'projectSeq': project_seq,
        'progress': project.get('progress'),
        'progressReason': project.get('progressReason'),
        'hasFailed': project.get('hasFailed'),
        'failureReason': project.get('failureReason'),
    }


# 5. Completed 이후 download?target=all로 .tar URL을 받습니다.
@app.get('/campaigns/{project_seq}/download')
async def perso_script_download(
    project_seq: int,
    space_seq: int = Query(..., gt=0),
):
    project = await call(
        'GET',
        f'{PREFIX}/projects/{project_seq}/spaces/{space_seq}',
    )

    if project.get('progressReason') != 'Completed':
        raise HTTPException(409, '더빙 작업이 아직 완료되지 않았습니다')

    download = await call(
        'GET',
        f'{PREFIX}/projects/{project_seq}/spaces/{space_seq}/download',
        params={'target': 'all'},
    )

    result = download.get('result')
    if not isinstance(result, dict):
        raise HTTPException(502, '다운로드 응답 형식이 올바르지 않습니다')

    path = result.get('zippedFileDownloadLink')
    if not isinstance(path, str) or not path:
        raise HTTPException(502, '.tar 다운로드 경로가 없습니다')

    return {
        'projectSeq': project_seq,
        'downloadUrl': file_url(path),
    }
# 6. 선택적으로 완료된 더빙 영상에 Lip Sync API를 연동합니다.
#
# Response body
# Download
# {
#   "mediaSeq": 954190,
#   "spaceSeq": 612722,
#   "kind": "video",
#   "fileName": "dubbing_presentation_en.mp4",
#   "size": 125455,
#   "azureHttpStatus": 201,
#   "message": "Perso 파일 등록 완료"
# }

#
# Response body
# Download
# {
#   "projectSeqList": [
#     447656,
#     447657
#   ],
#   "message": "프로젝트별 진행률을 별도로 확인하세요"
# }
