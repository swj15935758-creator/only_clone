# day50_application.py
# 주제:[Application 과제] 채용 공고에서 핵심 정보 추출하기
#
# 목표 : 비정형 채용 공고를 일정한 JSON 구조의 정답 데이터로 변경

import json
from pathlib import Path
import numpy as np
from util.print_util import pp, up

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / 'data'
REPORT_DIR = ROOT / 'reports'

def validate_sample(item):
    if not isinstance(item, dict):
        return False, '딕셔너리 형식이 아님'
    for field in ('instruction', 'input', 'output'):
        if field not in item or not isinstance(item[field], str):
            return False, f'{field} 누락 또는 문자열 형식 오류'
    if not item['instruction'].strip():
        return False, '지시가 비어 있음'
    if not item['output'].strip():
        return False, '정답이 비어 있음'

    valid, reason = validate_output(item['output'])
    if not valid:
        return False, reason

    return True, '정상'

def clean_samples(samples):
    accepted, rejected, seen = [], [], set()
    for row_number, item in enumerate(samples, start=1):
        valid, reason = validate_sample(item)
        if not valid:
            rejected.append({'row': row_number, 'reason': reason})
            continue
        cleaned = {field: item[field].strip() for field in ('instruction', 'input', 'output')}
        key = tuple(cleaned[field] for field in ('instruction', 'input', 'output'))
        if key in seen:
            rejected.append({'row': row_number, 'reason': '중복 데이터'})
            continue
        seen.add(key)
        accepted.append(cleaned)
    return accepted, rejected

def save_jsonl(path, rows):
    with path.open('w', encoding='utf8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

INSTRUCTION = "채용 공고에서 직무, 지역, 경력을 JSON으로 추출하세요"
JOBS = {"백엔드 개발자", "프론트엔드 개발자", "데이터 분석가", "AI 엔지니어", "QA 엔지니어"}
REGIONS = {"서울", "부산", "대전", "대구", "인천"}
EXPERIENCES = {"신입", "경력", "경력 무관"}

def validate_output(text):
    if not text.strip():
        return False, '출력 JSON이 비어 있음'

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False, 'JSON 문법 오류'

    if not isinstance(data, dict):
        return False, 'JSON 객체 형식이 아님'

    if set(data.keys()) != {'job', 'region', 'experience'}:
        return False, '필수 키 오류'

    for value in data.values():
        if not isinstance(value, str):
            return False, '값이 문자열이 아님'

    if data['job'].strip() not in JOBS:
        return False, '허용하지 않는 직무'

    if data['region'].strip() not in REGIONS:
        return False, '허용하지 않는 지역'

    if data['experience'].strip() not in EXPERIENCES:
        return False, '허용하지 않는 경력'

    return True, '정상'

SOURCE = [
    ("서울 백엔드 개발자 신입 채용", "백엔드 개발자", "서울", "신입"),
    ("부산 데이터 분석가 경력 3년 이상", "데이터 분석가", "부산", "경력"),
    ("대전 AI 엔지니어 경력 무관 채용", "AI 엔지니어", "대전", "경력 무관"),
    ("대구 프론트엔드 개발자 신입 모집", "프론트엔드 개발자", "대구", "신입"),
    ("인천 QA 엔지니어 경력 채용", "QA 엔지니어", "인천", "경력"),
    ("서울 데이터 분석가 신입 공고", "데이터 분석가", "서울", "신입"),
    ("대전 백엔드 개발자 경력자 채용", "백엔드 개발자", "대전", "경력"),
    ("부산 QA 엔지니어 경력 무관", "QA 엔지니어", "부산", "경력 무관"),
    ("인천 AI 엔지니어 신입 모집", "AI 엔지니어", "인천", "신입"),
    ("서울 백엔드 개발자 신입 채용", "백엔드 개발자", "서울", "신입"),
    ("대구 분석업무 모집", "데이터 분석가", "대구", ""),
]

RECORDS = [
    {
        'instruction': INSTRUCTION,
        'input': text,
        'output': json.dumps({
            'job': job,
            'region': region,
            'experience': experience
        }, ensure_ascii=False)
    }
    for text, job, region, experience in SOURCE
]

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    accepted, rejected = clean_samples(RECORDS)
    save_jsonl(DATA_DIR / 'application_jobs.jsonl', accepted)

    jobs_counts = {"백엔드 개발자": 0, "프론트엔드 개발자": 0, "데이터 분석가": 0, "AI 엔지니어": 0, "QA 엔지니어": 0}

    for item in accepted:
        output_data = json.loads(item['output'])
        jobs_counts[output_data['job']] += 1

    report = {
        'original_count': len(RECORDS),
        'accepted_count': len(accepted),
        'rejected_count': len(rejected),
        'rejected': rejected,
        'jobs_counts': jobs_counts
    }

    report_path = REPORT_DIR / 'application_jobs_report.json'
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding='utf8'
    )

    pp('원본 데이터: ', len(RECORDS))
    pp('정상 데이터: ', len(accepted))
    pp('제외 데이터: ', len(rejected))

    for issue in rejected:
        pp('제외 행: ', issue['row'], ', 제외 사유: ', issue['reason'])

    for job, count in jobs_counts.items():
        pp(job, ': ', count)

    pp('학습 데이터: ', DATA_DIR / 'application_jobs.jsonl')
    pp('품질 보고서: ', report_path)

if (__name__ == '__main__'):
    main()