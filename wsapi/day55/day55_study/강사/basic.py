# day55_basic.py
# Basic | 도서 대여 신청 API
# 주제: 음성 서비스와 무관한 도서관 대여 요청 관리
# 목표: FastAPI GET/POST, Path/Query, Pydantic BaseModel/Field, 404 및 201 처리
# 요구사항:
# BookLoan 모델: book_title(2~80자), borrower(2~30자), days(1~30일).
# POST /loans: 대여를 생성하고 201 및 자동 발급 ID를 반환합니다.
# GET /loans?limit=...: 1~50개만 목록을 반환합니다.
# GET /loans/{loan_id}: 없는 ID에는 404를 반환합니다.
# /docs에서 정상 입력 1개와 검증 실패 입력 2개를 확인합니다.

from uuid import uuid4
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from util.print_util import pp
app = FastAPI(title='Library Loan API')

LOANS = {}
# 대여 요청 책 제목 사용자대여 기간 유효성을 검사하는 BaseModel
class LoanInput(BaseModel):
    book_title: str = Field(min_length=2, max_length=80)
    borrow: str = Field(min_length=2, max_length=30)
    days: int = Field(ge=1, le=30)

# 생성 응답에 대여 아이디 추가한 모델
class LoanOutput(LoanInput):
    loan_id : str

@app.post("/loan", status_code=status.HTTP_201_CREATED, response_model=LoanOutput)
def create_loan(data: LoanInput):
    loan = LoanOutput(loan_id=uuid4().hex, **data.model_dump())
    LOANS[loan.loan_id] = loan
    pp('대여접수:',loan.loan_id)
    return loan # 4개 들어가 있음

@app.get("/loan",response_model=list[LoanOutput])
def list_loan(limit: int = Query(10, gt=0 , le=50)):
    return list(LOANS.values())[:limit]

@app.get("/loan/{loan_id}",response_model=LoanOutput)
def get_loan(loan_id: str):
    if loan_id not in LOANS:
        raise HTTPException(404,'대여 내역에 없습니다.')
    return LOANS[loan_id]