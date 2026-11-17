# day58_basic.py
# 주제: [Basic] 지역 관광안내의 실제 지원 언어와 TTS 모델 조회

import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

load_dotenv()

BASE = 'https://api.perso.ai'
PREFIX = '/video-translator/api/v1'
KEY = os.getenv('PERSO_API_KEY', '').strip()

app = FastAPI(title='basic 관광 안내 실제 지원 언어와 TTS 모델 조회')

# 비동기 클라이언트 생성 함수
def make_client(timeout: float = 60.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=timeout, follow_redirects=False)

# 응답을 딕셔너리로 반환
def parse_response(response: httpx.Response) -> dict:
    try:
        data = response.json() if response.content else {}
    except ValueError:
        if response.status_code < 400:
            raise HTTPException(502, 'Perso 응답이 JSON 형식이 아닙니다')
        data = {'message': response.text[:120]}

    if response.status_code >= 400:
        err = data if isinstance(data, dict) else {'message': str(data)}
        raise HTTPException(
            status_code=response.status_code,
            detail={
                'code': err.get('code', ''),
                'detailCode': err.get('detailCode', ''),
                'message': err.get('message', err.get('detail', '외부 API 오류')),
            },
        )

    if 300 <= response.status_code < 400:
        raise HTTPException(502, '예상하지 못한 Perso 리다이렉션입니다')

    if not isinstance(data, dict):
        raise HTTPException(502, '예상하지 못한 Perso 응답 형식')

    return data

# 요청하는 함수
async def call(method: str, path: str, *, params=None, json=None) -> dict:
    if not KEY:
        raise HTTPException(503, 'PERSO_API_KEY가 필요합니다')

    try:
        async with make_client() as client:
            response = await client.request(
                method,
                BASE + path,
                params=params,
                json=json,
                headers={'XP-API-KEY': KEY},
            )
    except httpx.TimeoutException as exc:
        raise HTTPException(504, 'Perso API 요청 시간 초과') from exc
    except httpx.RequestError as exc:
        raise HTTPException(502, 'Perso API 연결 오류') from exc

    return parse_response(response)

# 1. 보유한 API 키로 GET /video-translator/api/v1/languages를 호출합니다.
@app.get('/perso/languages')
async def get_langs():
    languages = await call('GET', f'{PREFIX}/languages')
    return languages
# 2. GET /guide/languages?code=ko&code=ja&model=LINNET_3을 작성합니다.
@app.get('/guide/languages')
async def get_guide(
    code: list[str] = Query(...),
    model: str = Query(...),
):
    requested_codes = [value.strip().lower() for value in code]
    requested_model = model.strip().upper()

    if not requested_model or any(not value for value in requested_codes):
        raise HTTPException(422, '언어 코드와 모델 이름을 입력하세요')

    if 'auto' in requested_codes:
        raise HTTPException(422, 'auto는 대상 언어로 사용할 수 없습니다')

    languages = await call('GET', f'{PREFIX}/languages')
    all_languages = languages.get('languages')

    if not isinstance(all_languages, list):
        raise HTTPException(502, 'Perso 언어 목록 형식이 올바르지 않습니다')

    result = []

    for requested_code in requested_codes:
        found = False

        for lang in all_languages:
            if not isinstance(lang, dict):
                raise HTTPException(502, 'Perso 언어 항목 형식이 올바르지 않습니다')

            if lang.get('code') != requested_code:
                continue

            found = True
            supported_models = lang.get('supportedTtsModels')

            if not isinstance(supported_models, list):
                raise HTTPException(502, 'TTS 모델 목록 형식이 올바르지 않습니다')

            result.append({
                'code': lang['code'],
                'name': lang.get('name'),
                'languageTag': lang.get('languageTag'),
                'supportedTtsModels': supported_models,
                'requestedModel': requested_model,
                'supported': requested_model in supported_models,
            })

        if not found:
            raise HTTPException(
                404,
                f'지원하지 않는 언어 코드: {requested_code}'
            )

    return result

# 3. supportedTtsModels를 실제 조회해 언어별 지원 여부를 표시합니다.
# 4. 같은 code에 여러 languageTag가 존재하면 모두 표시합니다.
# 5. 지원하지 않는 언어 코드=404, auto=422로 처리합니다.


# ====작성 코드====


