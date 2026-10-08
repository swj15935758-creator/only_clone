# day7_challenge.py

from pathlib import Path
import day7_challenge_uyils as cutils

DATA_DIR = Path('day7_challenge_uyils_data')
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / 'data.csv'

if not CSV_PATH.exists():
    cutils.save_sample_csv(CSV_PATH)

students = cutils.load_score_csv(CSV_PATH)

if len(students) > 0:
    # 리스트 컴프리헨션
    # students 안의 튜플에서 점수만 꺼내 새로운 리스트 생성
    # students 의 name, scire 에서 score 들로 리스트 구성
    scores = [score for name, score in students]
    student_count = len(scores) # 학생수
    total = sum(scores) # 총점
    average = total / student_count # 평균
    max_score = max(scores) # 최고점
    min_score = min(scores) # 최저점

    print(f'정상 학생수 : {student_count}명')
    print(f'평군 : {average}명')
    print(f'최고점 : {max_score}명')
    print(f'최저점 : {min_score}명')

    print('\n[pass 학생]')
    for name, score in students:
        if score >= 80:
            print(f'{name}: {score}점')

else:
    print('학생 데이터가 없어 통계를 계산하지 않습니다')