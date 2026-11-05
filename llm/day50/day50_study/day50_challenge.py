# day50_challenge.py
# 주제: [Challenge 과제] IT 보안 이벤트 위험도 분류 데이터 구축과 기준선 평가

import json
from pathlib import Path
from util.print_util import pp

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'data'
REPORT_DIR = ROOT / 'reports'

INSTRUCTION = "보안 이벤트 위험도를 높음, 보통, 낮음으로 분류하세요"

LABELS = {"높음", "보통", "낮음"}

EVENTS = [
    ("사내 파일 서버에서 랜섬웨어 의심 파일 발견", "높음"),
    ("관리자 계정에 외부인 침해 흔적 확인", "높음"),
    ("업무용 PC에서 데이터 유출 의심 행위 발견", "높음"),
    ("관리자 로그인 성공 후 낯선 해외 접속 탐지", "높음"),
    ("사내 메일로 악성 링크 신고 접수", "보통"),
    ("직원 계정의 로그인 실패 반복", "보통"),
    ("의심스러운 첨부파일 다운로드 시도", "보통"),
    ("공용 와이파이에서 비정상 접속 알림", "보통"),
    ("정기 보안 업데이트 정상 완료", "낮음"),
    ("예정된 서버 점검 작업 종료", "낮음"),
    ("백업 시스템 정상 동작 확인", "낮음"),
    ("사내 보안 교육 수강 완료", "낮음"),
    ("서버에서 대량의 파일이 암호화된 정황 확인", "높음"),
    ("반복 로그인 실패 신고 접수", "보통"),
    ("정기 시스템 점검 정상 완료", "낮음"),
    ("사내 파일 서버에서 랜섬웨어 의심 파일 발견", "높음"),
    ("정체불명의 이벤트", ""),
]

RECORDS = [
    {'instruction': INSTRUCTION, 'input': text, 'output': label}
    for text, label in EVENTS
]

def normalize_text(text):
    return ''.join(char for char in text.lower() if char.isalnum())

def validate_sample(item):
    if not isinstance(item, dict):
        return False, '딕셔너리 형식이 아님'

    for field in ('instruction', 'input', 'output'):
        if field not in item or not isinstance(item[field], str):
            return False, f'{field} 누락 또는 문자열 형식 오류'

    if not item['instruction'].strip():
        return False, '지시가 비어 있음'

    if not normalize_text(item['input']):
        return False, '입력이 비어 있음'

    if not item['output'].strip():
        return False, '정답이 비어 있음'

    if item['output'].strip() not in LABELS:
        return False, '허용하지 않는 정답'

    return True, '정상'

def clean_samples(samples):
    accepted, rejected, seen = [], [], set()

    for row_number, item in enumerate(samples, start=1):
        valid, reason = validate_sample(item)

        if not valid:
            rejected.append({'row': row_number, 'reason': reason})
            continue

        cleaned = {
            field: item[field].strip()
            for field in ('instruction', 'input', 'output')
        }

        key = normalize_text(cleaned['input'])

        if key in seen:
            rejected.append({'row': row_number, 'reason': '중복 입력 데이터'})
            continue

        seen.add(key)
        accepted.append(cleaned)

    return accepted, rejected

def save_jsonl(path, rows):
    with path.open('w', encoding='utf8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

def baseline_predict(text):
    if '랜섬웨어' in text or '침해' in text or '유출' in text:
        return '높음'

    if '악성 링크' in text or '로그인 실패' in text or '첨부파일' in text or '비정상 접속' in text:
        return '보통'

    return '낮음'

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    accepted, rejected = clean_samples(RECORDS)

    train_samples = []
    test_samples = []

    for label in ('높음', '보통', '낮음'):
        label_samples = [
            item for item in accepted
            if item['output'] == label
        ]

        split_index = round(len(label_samples) * 0.6)

        train_samples.extend(label_samples[:split_index])
        test_samples.extend(label_samples[split_index:])

    train_inputs = {normalize_text(item['input']) for item in train_samples}
    test_inputs = {normalize_text(item['input']) for item in test_samples}

    if train_inputs & test_inputs:
        raise ValueError('Train과 Test에 중복 입력이 존재합니다.')

    save_jsonl(DATA_DIR / 'challenge_train.jsonl', train_samples)
    save_jsonl(DATA_DIR / 'challenge_test.jsonl', test_samples)

    correct = 0
    errors = []

    for item in test_samples:
        prediction = baseline_predict(item['input'])
        answer = item['output']

        if prediction == answer:
            correct += 1
        else:
            errors.append({
                'input': item['input'],
                'answer': answer,
                'prediction': prediction
            })

    accuracy = correct / len(test_samples) if test_samples else 0

    report = {
        'original_count': len(RECORDS),
        'accepted_count': len(accepted),
        'rejected_count': len(rejected),
        'train_count': len(train_samples),
        'test_count': len(test_samples),
        'correct_count': correct,
        'accuracy': round(accuracy, 4),
        'rejected': rejected,
        'errors': errors
    }

    report_path = REPORT_DIR / 'challenge_security_report.json'
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding='utf8'
    )

    pp('원본 데이터: ', len(RECORDS))
    pp('정상 데이터: ', len(accepted))
    pp('제외 데이터: ', len(rejected))

    for issue in rejected:
        pp('제외 행: ', issue['row'], ', 제외 사유: ', issue['reason'])

    pp('Train 데이터: ', len(train_samples))
    pp('Test 데이터: ', len(test_samples))
    pp('정답 건수: ', correct)
    pp('Accuracy: ', round(accuracy, 4))

    for error in errors:
        pp('오분류 입력: ', error['input'])
        pp('실제 정답: ', error['answer'])
        pp('예측 결과: ', error['prediction'])

    pp('학습 데이터: ', DATA_DIR / 'challenge_train.jsonl')
    pp('평가 데이터: ', DATA_DIR / 'challenge_test.jsonl')
    pp('품질 보고서: ', report_path)

if __name__ == '__main__':
    main()