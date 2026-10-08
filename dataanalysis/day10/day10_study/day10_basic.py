# Day 10 Basic 과제 - 직원 교육 참석 데이터 점검
# 예상 수행시간: 25분
#
# [상황]
# 인사팀에서 직원 교육 참석 현황 CSV 데이터를 전달받았습니다. 분석을 시작하기 전에 파일이 정상적으로 읽히는지, 어떤 컬럼이 있는지, 데이터가 몇 행인지 확인해야 합니다.
#
# [데이터]
# 아래 데이터를 코드 안에서 DataFrame으로 만든 뒤 employee_training.csv로 저장하여 사용하십시오.
#
# 사번,이름,부서,교육점수,교육시간
# E101,김지훈,개발,88,8
# E102,이수빈,기획,92,10
# E103,박현우,영업,76,6
# E104,정예린,개발,95,12
# E105,최민석,기획,84,8
# E106,한서진,영업,81,7
#
# [문제]
# pandas를 pd로 불러오십시오.
# 제시된 데이터를 DataFrame으로 만든 뒤 employee_training.csv 파일로 저장하십시오.
# pd.read_csv()로 CSV 파일을 다시 읽어 employee_df에 저장하십시오.
# 처음 3개 행과 마지막 2개 행을 각각 출력하십시오.
# employee_df의 행 수와 열 수를 각각 출력하십시오.
# 모든 컬럼 이름을 리스트 형태로 출력하십시오.
# 각 컬럼의 dtype을 출력하십시오.
# info()를 이용해 데이터 구조를 확인하십시오.
# 교육점수의 평균, 최솟값, 최댓값을 출력하십시오.
# 부서별 직원 수를 value_counts()로 출력하십시오.
#
# [제출 조건]
# 실습에서 사용한 학생 데이터와 다른 업무 상황으로 작성할 것
# 각 출력 구간의 목적을 주석으로 설명할 것
# 결과가 한눈에 구분되도록 제목 또는 구분선을 출력할 것

# day10_basic.py

import pandas as pd

# 직원 교육 데이터 딕셔너리
training_data = {
    "사번": ["E101", "E102", "E103", "E104", "E105", "E106"],
    "이름": ["김지훈", "이수빈", "박현우", "정예린", "최민석", "한서진"],
    "부서": ["개발", "기획", "영업", "개발", "기획", "영업"],
    "교육점수": [88, 92, 76, 95, 84, 81],
    "교육시간": [8, 10, 6, 12, 8, 7],
}

# 딕셔너리 > 데이터프레임
source_df = pd.DataFrame(training_data)

# 데이터프레임 > CSV 파일
source_df.to_csv('employee_training.csv', index=False, encoding='utf-8-sig')

# CSV 파일 > 데이터프레임
employee_df = pd.read_csv('employee_training.csv', encoding='utf-8-sig')

print(employee_df.head(3)) # 상위 3개 행

print(employee_df.tail(2)) # 하위 2개 행

print('행 수: ', employee_df.shape[0]) # 6

print('행 수: ', employee_df.shape[1]) # 5

#  ['사번', '이름', '부서', '교육점수', '교육시간']
print('컬럼: ', list(employee_df.columns))

print(employee_df.dtypes) # 컬럼 데이터타입

employee_df.info() # 전체 구조

score = employee_df['교육점수'] # 교육점수 컬럼 시리즈
print(f'평균: {score.mean():.2f}') # 교육점수 평균 소수 두째자리
print('최소값: ', score.min())
print('최대값: ', score.max())
print(employee_df['부서'].value_counts()) # 부서별 직원 수




