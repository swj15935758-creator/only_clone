# day50_basic.py
# 대학 학사 공지의 분류형 지시학습 데이터 생성과 정제

import json
from collections import Counter
from pathlib import Path
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

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

RECORDS = [{"instruction": INSTRUCTION, "input": text, "output": label} for text, label in RAW]

# 학사 공지 데이터의 필수 키와 분류 값의 적합성을 검사하는 함수
# record: instruction/input/output 딕셔너리
# 반환값: (정상여부 bool, 오류 사유 str)
def validate_record(record):
    if not isinstance(record, dict):
        return False, '딕셔너리가 아님'
    for field in ("instruction", "input", "output"):
        if field not in record or not isinstance(record[field], str):
            return False, f'{field} 필드 누락 또는 자료형 오류'
    if not record["instruction"].strip() or not record["input"].strip():
        return False, '지시 또는 공지가 비어 있음'
    if record['output'].strip() not in CATEGORIES:
        return False, '허용되지 않은 정답 카테고리'
    return True, '정상'

# 입력 레코드를 검사하고 공백/중복 문제를 제거하는 함수
# records: 검사할 원본 딕셔너리 리스트
# 반환값: (정상 고유 레코드 리스트, 제외 사유 리스트)
def clean_record(records):
    accepted, rejected, seen = [], [], set()
    for number, record in enumerate(records, start=1):
        valid, reason = validate_record(record)
        if not valid:
            rejected.append({'row': number, 'reason': reason})
            continue
        clean = {key: record[key].strip() for key in ('instruction', 'input', 'output')}
        key = (clean['instruction'], clean['input'], clean['output'])
        if key in seen:
            rejected.append({'row': number, 'reason': '중복 레코드'})
            continue
        seen.add(key)
        accepted.append(clean)
    return accepted, rejected

# 딕셔너리 목록을 한 줄당 한건인 JSONL 파일로 저장하는 함수
# rows: 기록할 딕셔너리 리스트
def save_jsonl(path, rows):
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

def main():

    data_dir, report_dir = ROOT / 'data', ROOT / 'report'
    data_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    accepted, rejected = clean_record(RECORDS)

    save_jsonl(data_dir / 'basic_campus_train.jsonl', accepted)

    counts = dict(Counter(row['output'] for row in accepted))

    report = {
        'total': len(RECORDS),
        'accepted': len(accepted),
        'rejected': len(rejected),
        'category_counts': counts
    }

    (report_dir / 'basic_campus_report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

    pp('정상: ', len(accepted), ', 제외: ', len(rejected))
    pp('분류별 건수: ', counts)
    pp('제외 사유: ', rejected)

if __name__ == '__main__':
    main()