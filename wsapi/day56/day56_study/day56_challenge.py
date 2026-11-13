# day56_challenge.py
# Challenge: 환율 참고정보 집계 API

import math
from datetime import date

import httpx
from fastapi import APIRouter, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, ValidationError

# 요구사항
# https://api.frankfurter.dev/v1/latest (공개 환율 조회 서비스 URL)
# GET /rates/{base}: 외부 Frankfurter 공개 API의 통화별 환율을 조회합니다.
# GET /convert?base=USD&quote=KRW&amount=10: 환산 금액을 반환합니다.
# httpx.Client, timeout, raise_for_status, 응답 검사와 HTTP 오류 변환 구현
# 값이 양수인지 Pydantic/Query 검증하고 통화코드는 정규화합니다.
# 호출 실패에 502, 시간 초과에 504를 반환합니다.
# 비밀키는 필요 없습니다. 외부 응답 구조나 정책 변경 시 오류를 명시합니다.

FRANKFURTER_URL = 'https://api.frankfurter.dev/v1/latest'

app = FastAPI(
    title='환율 참고정보 API',
    version='0.0.1'
)

rate_router = APIRouter(tags=['rates'])

class RateResponse(BaseModel):
    amount: float = Field(gt=0)
    base: str
    date: date
    rates: dict[str, float]

def normalize_currency(currency):
    normalized = currency.strip().upper()

    if (
        len(normalized) != 3
        or not normalized.isascii()
        or not normalized.isalpha()
    ):
        raise HTTPException(422, '통화 코드는 영문자 3자리여야 합니다.')

    return normalized

def fetch_rates(base, quote=None):
    params = {'base': base}

    if quote is not None and quote != base:
        params['symbols'] = quote

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(FRANKFURTER_URL, params=params)
            response.raise_for_status()
            raw_data = response.json()

    except httpx.TimeoutException:
        raise HTTPException(504, 'Frankfurter 응답시간 초과')

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            502,
            f'Frankfurter API HTTP {exc.response.status_code}'
        )

    except httpx.RequestError:
        raise HTTPException(502, 'Frankfurter API 연결 실패')

    except ValueError:
        raise HTTPException(502, 'Frankfurter 응답이 JSON이 아닙니다.')

    try:
        data = RateResponse.model_validate(raw_data)
    except ValidationError:
        raise HTTPException(502,'Frankfurter 응답 구조가 예상과 다릅니다.')

    if data.base != base or data.amount != 1:
        raise HTTPException(502, 'Frankfurter의 기준 통화 또는 기준 금액이 예상과 다릅니다.')

    for currency, rate in data.rates.items():
        if not currency or not math.isfinite(rate) or rate <= 0:
            raise HTTPException(502, 'Frankfurter 응답에 잘못된 환율이 있습니다.')

    return data

@rate_router.get('/rates/{base}')
def get_rates(base: str):
    base = normalize_currency(base)
    data = fetch_rates(base)
    return data

@rate_router.get('/convert')
def convert_currency(
    base: str = Query(default='USD'),
    quote: str = Query(default='KRW'),
    amount: float = Query(10, gt=0)
):
    base = normalize_currency(base)
    quote = normalize_currency(quote)

    if not math.isfinite(amount):
        raise HTTPException(422, '금액은 유한한 양수여야 합니다.')

    data = fetch_rates(base, quote)

    if base == quote:
        rate = 1.0
    else:
        rate = data.rates.get(quote)

        if rate is None:
            raise HTTPException(502, 'Frankfurter 응답에 대상 통화 환율이 없습니다.')

    return {
        'date': data.date,
        'base': base,
        'quote': quote,
        'amount': amount,
        'rate': rate,
        'converted_amount': round(amount * rate, 2)
    }

app.include_router(rate_router)