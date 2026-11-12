# day55_challenge.py
# 주제:Challenge | 행사 좌석 예약 API 행사 예약·좌석 수량 검증과 충돌 처리
#
# 목표: 상태 코드 201/404/409/422, API 응답 일관성 유지
#
# 요구사항:
# 행사 목록은 고정된 event_id, title, capacity로 정의합니다.
# POST /reservations: event_id, guest_name(2~40자), seats(1~4).
# 남은 좌석 수보다 많이 예약하면 409 Conflict를 반환합니다.
# GET /reservations/{reservation_id}: 예약 상세 및 404 처리.
# DELETE /reservations/{reservation_id}: 좌석 복원 및 예약 삭제.
# GET /events: 행사별 남은 좌석과 전체 좌석을 함께 표시합니다.
# 순서대로 2석 예약→초과 예약→취소→재예약을 직접 검증합니다.
#
#
# EVENTS = {
#     1: {"title": "Python 취업 특강", "capacity": 5},
#     2: {"title": "AI 프로젝트 발표회", "capacity": 8},
# }
