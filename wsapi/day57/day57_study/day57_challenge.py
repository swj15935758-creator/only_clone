# day57_challenge.py
# 주제: Challenge: 여행 일정 추천 마이크로서비스와 CLI 호출기
# 기존 캠퍼스 분류/WAV/Perso 언어 조회와 다른 '여행 코스 추천' 주제입니다.
# uvicorn day57_challenge_sol:app --reload --port 8003
import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

PLACES = {
    '서울': {'역사': '경복궁', '자연': '서울숲', '음식': '광장시장'},
    '부산': {'역사': '감천문화마을', '자연': '해운대', '음식': '부평깡통시장'},
}

app = FastAPI(title='여행 일정 추천 API')


class TripRequest(BaseModel):
    city: str = Field(min_length=1)
    days: int = Field(ge=1, le=5)
    interests: list[Literal['역사', '자연', '음식']] = Field(min_length=1, max_length=3)


class DayRecommendation(BaseModel):
    day: int
    interest: str
    place: str


class TripResponse(BaseModel):
    city: str
    days: int
    recommendations: list[DayRecommendation]


@app.post('/trip/recommend', response_model=TripResponse)
def recommend_trip(
    request: TripRequest,
    travel_key: str | None = Header(default=None, alias='X-Travel-Key'),
):
    expected_key = os.getenv('TRAVEL_API_KEY', '').strip()
    if not expected_key:
        raise HTTPException(503, '서버 API 키가 설정되지 않았습니다.')
    if travel_key != expected_key:
        raise HTTPException(401, 'API 키가 없거나 올바르지 않습니다.')

    city_places = PLACES.get(request.city)
    if city_places is None:
        raise HTTPException(404, '지원하지 않는 도시입니다.')

    recommendations = []
    for day in range(1, request.days + 1):
        interest = request.interests[(day - 1) % len(request.interests)]
        recommendations.append(DayRecommendation(
            day=day,
            interest=interest,
            place=city_places[interest],
        ))

    return TripResponse(
        city=request.city,
        days=request.days,
        recommendations=recommendations,
    )