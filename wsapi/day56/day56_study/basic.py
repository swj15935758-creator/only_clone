from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title='도서 예약 API')
router = APIRouter(prefix='/reservations',tags=['reservations'])
store = {} # 프로세스 종료시 초기화 되는 학습용 저장소

next_id = 1
class ReservationIn(BaseModel):
    book: str = Field(min_length=2, max_length=80)
    requester: str = Field(min_length=2, max_length=30)

@router.post('', status_code=201, response_model=ReservationIn)
def reserve(data: ReservationIn):
    global next_id
    item = {'id': next_id, **data.model_dump()}
    store[next_id] = item
    next_id += 1
    return item

@router.get('')
def all_reservations():
    return list(store.values())

@router.get('/{reservation_id}')
def get_reservation(reservation_id: int):
    if reservation_id not in store:
        raise HTTPException(404, '예약을 찾을 수 없습니다')
    return store[reservation_id]

@router.delete('/{reservation_id}')
def cancel_reservation(reservation_id: int):
    if reservation_id not in store:
        raise HTTPException(404, '예약을 찾을 수 없습니다')
    store.pop(reservation_id)
    return {'deleted': True,'id': reservation_id}

app.include_router(router)












