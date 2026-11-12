# day55_basic.py
# 주제:Basic | 도서 대여 신청 API 음성 서비스와 무관한 도서관 대여 요청 관리
#
# 목표: FastAPI GET/POST, Path/Query, Pydantic BaseModel/Field, 404 및 201 처리
#
# 요구사항:
# BookLoan 모델: book_title(2~80자), borrower(2~30자), days(1~30일).
# POST /loans: 대여를 생성하고 201 및 자동 발급 ID를 반환합니다.
# GET /loans?limit=...: 1~50개만 목록을 반환합니다.
# GET /loans/{loan_id}: 없는 ID에는 404를 반환합니다.
# /docs에서 정상 입력 1개와 검증 실패 입력 2개를 확인합니다.
