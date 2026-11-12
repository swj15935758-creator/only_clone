# day55_basic.py
# 주제: Basic | 도서 대여 신청 API 음성 서비스와 무관한 도서관 대여 요청 관리

from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

# 목표: FastAPI GET/POST, Path/Query, Pydantic BaseModel/Field, 404 및 201 처리
app = FastAPI(
    title='basic 오후 문제 풀이',
    description='basic',
    version='0.0.1',
)

# BookLoan 모델: book_title(2~80자), borrower(2~30자), days(1~30일).
class BookLoan(BaseModel):
    book_title: str = Field(min_length=2, max_length=80)
    borrower: str = Field(min_length=2, max_length=30)
    days: int = Field(ge=1, le=30)

class BookLoanOut(BookLoan):
    id: int

loans: dict[int, dict] = {}
next_loan_id = 1

# POST /loans: 대여를 생성하고 201 및 자동 발급 ID를 반환합니다.
@app.post('/loans', response_model=BookLoanOut, status_code=status.HTTP_201_CREATED)
def create_book_loan(book_loan: BookLoan):
    global next_loan_id
    new_loan = book_loan.model_dump()
    new_loan['id'] = next_loan_id
    loans[next_loan_id] = new_loan
    next_loan_id += 1
    return new_loan

# GET /loans?limit=...: 1~50개만 목록을 반환합니다.
@app.get('/loans', response_model=list[BookLoanOut])
def book_list(limit: int = Query(10, ge=1, le=50)):
    return list(loans.values())[:limit]

# GET /loans/{loan_id}: 없는 ID에는 404를 반환합니다.
@app.get('/loans/{loan_id}', response_model=BookLoanOut)
def get_book_loan(loan_id: Annotated[int, Path(ge=1)]):
    if loan_id not in loans:
        raise HTTPException(status_code=404, detail='대여 신청을 찾을 수 없습니다.')
    return loans[loan_id]