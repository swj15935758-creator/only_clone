# day50_basic.py
# 주제:[Basic 과제] 대학 캠퍼스 공지사항 분류 데이터셋 만들기
#
# 목표 : 학사 공지를 일정한 카테고리로 분류하기 위한 지시학습 데이터 제작

import json
from pathlib import Path
import numpy as np
from util.print_util import pp, up


# 상황
# 대학 행정실의 공지사항을 AI가 아래 세 카테고리로 분류하도록 준비함.
# 수업 : 강의실 변경, 휴강, 보강
# 장학 : 장학금 신청 및 선발
# 시설 : 도서관, 체육관, 교내 건물 이용

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / 'data' # 학습 데이터 저장 폴더

REPORT_DIR = ROOT / 'reports' # 품질 검사 보고서 저장 폴더

# 요구사항
# 최소 9건의 학사 공지를 딕셔너리 리스트로 작성
# instruction은 '학사 공지를 수업, 장학, 시설 중 하나로 분류하세요' 사용
# 동일 레코드 1건과 빈 output 1건을 포함해 데이터 오류 재현

# validate_record(record) : 필수 필드 및 문자열 검사, 빈 정답 제외
# 한 건의 지시학습 데이터(딕셔너리 1개)에서 필수 필드와 값의 형식을 검사하는 함수
def validate_sample(item):
    if not isinstance(item, dict):
        return False, '딕셔너리 형식이 아님' # 검증 성공 여부, 검증 메시지
    for field in ('instruction', 'input', 'output'):
        # 필드명(키)이 딕셔너리에 없거나 필드값(값)이 문자열이 아니면
        if field not in item or not isinstance(item[field], str):
            return False, f'{field} 누락 또는 문자열 형식 오류'
    if not item['instruction'].strip():
        return False, '지시가 비어 있음'
    if not item['output'].strip():
        return False, '정답이 비어 있음'
    return True, '정상'

# clean_records(records) : 앞뒤 공백 정리 후 중복 제거, 제외 사유 기록
def clean_samples(samples):
    accepted, rejected, seen = [], [], set()
    for row_number, item in enumerate(samples, start=1):
        valid, reason = validate_sample(item)
        if not valid:
            rejected.append({'row': row_number, 'reason': reason})
            continue
        cleaned = {field: item[field].strip() for field in ('instruction', 'input', 'output')}
        key = tuple(cleaned[field] for field in ('instruction', 'input', 'output'))
        if key in seen: # 이미 처리했다면
            rejected.append({'row': row_number, 'reason': '중복 데이터'})
            continue
        seen.add(key)
        accepted.append(cleaned)
    return accepted, rejected

# data/basic_campus_train.jsonl 에 정상 데이터 저장
def save_jsonl(path, rows):
    with path.open('w', encoding='utf8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

# reports/basic_campus_report.json 에 전체·정상·제외 건수, 제외 사유 저장
# 검증 결과와 카테고리별 건수를 pp()로 출력


# 완료 확인
# JSONL 파일을 텍스트 편집기로 열면 한 줄에 하나의 JSON 객체가 존재
# 데이터 오류가 적절한 이유와 함께 제외됨
# 고객 문의·배송·환불 등의 데이터는 사용하지 않음
INSTRUCTION = "학사 공지를 수업, 장학, 시설 중 하나로 분류하세요"

CATEGORIES = {"수업", "장학", "시설"}

RAW = [
    ("오늘 프로그래밍 강의실이 301호로 변경되었습니다", "수업"),
    ("자료구조 수업은 학과 행사로 휴강합니다", "수업"),
    ("금요일 알고리즘 보강 수업을 진행합니다", "수업"),
    ("국가장학금 신청 기간이 시작되었습니다", "장학"),
    ("교내 성적우수장학생 명단을 안내합니다", "장학"),
    ("근로장학금 신청서를 제출하세요", "장학"),
    ("중앙도서관 열람실 운영 시간을 연장합니다", "시설"),
    ("체육관 바닥 보수로 이용이 제한됩니다", "시설"),
    ("학생회관 출입문 공사를 진행합니다", "시설"),
    ("오늘 프로그래밍 강의실이 301호로 변경되었습니다", "수업"),
    ("다음 학기 장학 심사 안내", " "),
]

RECORDS = [{"instruction": INSTRUCTION, "input": text,
            "output": label} for text, label in RAW]


def main():

    DATA_DIR.mkdir(exist_ok=True, parents=True)
    REPORT_DIR.mkdir(exist_ok=True, parents=True)

    accepted, rejected = clean_samples(RECORDS)
    save_jsonl(DATA_DIR / 'basic_campus_train.jsonl', accepted)

    category_counts = {'수업': 0, '장학': 0, '시설': 0}

    for item in accepted:
        category_counts[item['output']] += 1

    report = {
        'original_count': len(RECORDS),
        'accepted_count': len(accepted),
        'rejected_count': len(rejected),
        'rejected': rejected,
        'category_counts': category_counts
    }

    report_path = REPORT_DIR / 'basic_campus_report.json'
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding='utf8'
    )

    pp('원본 데이터: ', len(RECORDS))
    pp('정상 데이터: ', len(accepted))
    pp('제외 데이터: ', len(rejected))

    for issue in rejected:
        pp('제외 행: ', issue['row'], ', 제외 사유: ', issue['reason'])

    for category, count in category_counts.items():
        pp(category, ': ', count)

    pp('학습 데이터: ', DATA_DIR / 'basic_campus_train.jsonl')
    pp('품질 보고서: ', report_path)

if __name__ == '__main__':
    main()
