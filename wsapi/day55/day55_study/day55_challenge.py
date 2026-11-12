# day55_challenge.py
# 주제:Challenge | 행사 좌석 예약 API 행사 예약·좌석 수량 검증과 충돌 처리
from threading import Lock
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field


app = FastAPI(title='행사 좌석 예약 API')

EVENTS = {
    1: {"title": "Python 취업 특강", "capacity": 5},
    2: {"title": "AI 프로젝트 발표회", "capacity": 8},
}

# 목표: 상태 코드 201/404/409/422, API 응답 일관성 유지
# 요구사항:
# 행사 목록은 고정된 event_id, title, capacity로 정의합니다.
# POST /reservations: event_id, guest_name(2~40자), seats(1~4).
class ReservationIn(BaseModel):
    event_id: int
    guest_name: str = Field(min_length=2, max_length=40)
    seats: int = Field(ge=1, le=4)

class ReservationOut(ReservationIn):
    reservation_id: int

class EventOut(BaseModel):
    event_id: int
    title: str
    capacity: int
    remaining_seats: int

class CancellationOut(BaseModel):
    reservation_id: int
    message: str

# 남은 좌석 수보다 많이 예약하면 409 Conflict를 반환합니다.
# GET /reservations/{reservation_id}: 예약 상세 및 404 처리.
# DELETE /reservations/{reservation_id}: 좌석 복원 및 예약 삭제.
# GET /events: 행사별 남은 좌석과 전체 좌석을 함께 표시합니다.
# 순서대로 2석 예약→초과 예약→취소→재예약을 직접 검증합니다.


remaining_seats = {
    event_id: event['capacity'] for event_id, event in EVENTS.items()
}
reservations: dict[int, dict] = {}
next_reservation_id = 1
state_lock = Lock()

@app.post('/reservations', response_model=ReservationOut,
          status_code=status.HTTP_201_CREATED)
def create_reservation(data: ReservationIn):
    global next_reservation_id

    with state_lock:
        if data.event_id not in EVENTS:
            raise HTTPException(status_code=404, detail='행사를 찾을 수 없습니다.')

        if data.seats > remaining_seats[data.event_id]:
            raise HTTPException(status_code=409, detail='남은 좌석이 부족합니다.')

        reservation = data.model_dump()
        reservation['reservation_id'] = next_reservation_id
        reservations[next_reservation_id] = reservation
        remaining_seats[data.event_id] -= data.seats
        next_reservation_id += 1
        return reservation

@app.get('/reservations/{reservation_id}', response_model=ReservationOut)
def get_reservation(reservation_id: int = Path(ge=1)):
    with state_lock:
        if reservation_id not in reservations:
            raise HTTPException(status_code=404, detail='예약을 찾을 수 없습니다.')
        return reservations[reservation_id].copy()

@app.delete('/reservations/{reservation_id}', response_model=CancellationOut)
def delete_reservation(reservation_id: int = Path(ge=1)):
    with state_lock:
        if reservation_id not in reservations:
            raise HTTPException(status_code=404, detail='예약을 찾을 수 없습니다.')

        reservation = reservations[reservation_id]
        remaining_seats[reservation['event_id']] += reservation['seats']
        del reservations[reservation_id]
        return {'reservation_id': reservation_id, 'message': '예약 취소 완료'}

@app.get('/events', response_model=list[EventOut])
def list_events():
    with state_lock:
        events = []
        for event_id, event in EVENTS.items():
            events.append({
                'event_id': event_id,
                'title': event['title'],
                'capacity': event['capacity'],
                'remaining_seats': remaining_seats[event_id]
            })
        return events