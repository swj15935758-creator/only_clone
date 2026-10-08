import csv
from pathlib import Path


DATA_DIR = Path('day7_application_강사님코드_data')
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / 'student_scores.csv'


def create_sample_csv(path):
    # CSV에 저장할 2차원 리스트
    rows = [
        ['name', 'score'],
        ['김민수', 88],
        ['이서현', 93],
        ['박지훈', 76],
        ['최유진', 85]
    ]

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# 파일을 읽어서 데이터 리스트를 반환 하는 함수
def load_scores(path):
    # 정상 데이터 저장 리스트
    result = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            # 헤더라인
            header = next(reader)
            print('csv 헤더', header)

            # 데이터행 반복
            for row in reader:
                name = row[0].strip()
                score = int(row[1])

                # 이름과 점수를 튜플로 만들어 리스트에 추가
                result.append((name, score))
    except FileNotFoundError: # 파일이 없을떄
        print('성적 파일을 찾을 수 없습니다.')
    except ValueError: # int로 정수 변환 할떄
        print('점수는 숫자로 입력 되어야 합니다.')

    return result # 리스트 반환


if not CSV_PATH.exists():# CSV 경로가 없다면
    create_sample_csv(CSV_PATH) # 생성
scores = load_scores(CSV_PATH) # 리스트 반환

if len(scores) > 0: # 데이터가 있다면
    print('\n[학생별 점수]') #제목 출력
    for name, score in scores: # 리스트내의 튜플 수만큼 반복
        print(f'{name} : {score}점')
    total = sum(score for name, score in scores) # 총점 강사님이 쓰지 말라한거 같지만...
    average = total / len(scores)  # 평균
    print(f'\n평균점수: {average:.2f}점') # 소수점 두째 자리까지 평균 출력
else:#  데이터가 없다
    print('계산항 데이터가 없습니다.')














