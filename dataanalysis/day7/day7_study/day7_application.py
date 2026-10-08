# day7_application.py

import csv
from pathlib import Path


# 1. CSV 파일이 들어갈 폴더 만들기
DATA_DIR = Path('day7_application_data')
DATA_DIR.mkdir(exist_ok=True)

# 2. CSV 파일 경로 만들기
SCORE_PATH = DATA_DIR / 'student_scores.csv'


# 3. CSV 파일에 저장할 샘플 데이터
students = [
    ['name', 'score'],
    ['김민수', 88],
    ['이서현', 93],
    ['박지훈', 76],
    ['최유진', 85]
]


# 4. CSV 파일 생성하고 데이터 저장하기
with open(SCORE_PATH, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(students)


# 5. CSV 파일을 읽는 함수
def load_scores(path):
    # 정상적으로 읽은 학생 정보를 저장할 리스트
    score_list = []

    try:
        # CSV 파일 읽기
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            # CSV 파일을 한 줄씩 읽기
            for row in reader:

                # name, score 제목 줄이 아닌 경우만 실행
                if row[0] != 'name':
                    name = row[0]
                    score = int(row[1])

                    # (이름, 점수) 형태로 리스트에 추가
                    score_list.append((name, score))

    # 파일이 존재하지 않을 경우
    except FileNotFoundError:
        print('성적 파일이 존재하지 않습니다.')

    # 점수를 정수로 변환할 수 없는 경우
    except ValueError:
        print('점수에 숫자가 아닌 값이 들어 있습니다.')

    # 읽은 학생 정보 반환
    return score_list


# 6. load_scores 함수 실행
students = load_scores(SCORE_PATH)


# 7. 학생별 점수 출력
for student in students:
    name = student[0]
    score = student[1]

    print(f'{name}님: {score}점')


# 8. 정상 데이터가 1건 이상이면 평균 계산
if len(students) > 0:
    total_score = 0

    # 학생들의 점수를 하나씩 더하기
    for student in students:
        total_score = total_score + student[1]

    # 평균 = 총점 / 학생 수
    average = total_score / len(students)

    print(f'평균 점수: {average}점')

else:
    print('계산할 데이터가 없습니다.')