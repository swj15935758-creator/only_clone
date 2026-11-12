# day55_application.py
# 주제:Application | 채용 공고 검색 API 취업 공고 등록과 기술 스택 필터링
#
# 목표: REST 자원 설계, Enum/Field 검증, 응답 모델과 예외 처리
#
# 요구사항:
# JobPost 입력: company(2~50자), position(2~60자), level(junior/mid),
# skills(1~8개), salary_min(0 이상 정수).
# POST /posts: 공고를 생성하고 201 반환.
# GET /posts?skill=python&min_salary=3000: 선택적 필터와 최소 급여 조건.
# GET /posts/{post_id}: 없는 공고는 404.
# DELETE /posts/{post_id}: 삭제 성공 후 간결한 JSON 응답.
