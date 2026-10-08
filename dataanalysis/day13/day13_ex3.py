# day13_ex3.py
# 문자열 처리, 범주형, 구간화 보충
from python.print_util import pp
import pandas as pd

# str.conatin() 와 na=False
s = pd.Series(['AI 개발','python',None,'생성형 AI'])
pp(s)
# 'AI' 문자열을 포함하면 True 아니면 False 불리언 값을 갖는 시리즈
pp(s.str.contains('AI'))
pp(type(s.str.contains('AI')))
pp(s.str.contains('AI',na=False)) # 결측치를 False
pp(type(s.str.contains('AI',na=False)))

# str.split() 과 expand=True
dates = pd.Series([
    '2026-09-08','2025-12-25','2024-01-01',
])
pp(dates)
pp(dates.str.split('-'))
pp(type(dates.str.split('-'))) # <class 'pandas.Series'>
pp(dates.str.split('-',expand=True)) # 열 확장
pp(type(dates.str.split('-',expand=True))) #<class 'pandas.DataFrame'>

# str.extract() 와 챕춰그룹()
s = pd.Series(['상품123','제품45','item789'])
pp(s)
# 패턴을 따르는 문자열을 추출(extract)하려면 추출 하기 전에 캡춰를 해야 함
pp(s.str.extract(r'(\d+)')) # 숫자가 하나 이상 나오는 문자열을 캡춰(저장)
pp(type(s.str.extract(r'(\d+)'))) # <class 'pandas.DataFrame'>
date_text = pd.Series([
    '2026-09-08','2025-12-25','2024-01-01',
])
# 여러 문자열 동시 캡춰
result = date_text.str.extract(r'(\d{4})-(\d{2})-(\d{2})')
pp(result)
pp(type(result))  #<class 'pandas.DataFrame'>


# category 타입과 cat 접근자
s = pd.Series(
    pd.Categorical(
        ['중', '상', '하', '중'],  # 실제 데이터
        categories=['하', '중', '상', '최상'],  # 사용 가능한 범주
    )
)
pp(s)
pp(type(s)) # <class 'pandas.Series'>

#Index(['하', '중', '상', '최상'], dtype='str')
# Decorator 패턴 : 인덱스 안에 (dtype, 리스트) 가 들어있는거
pp(s.cat.categories)
pp(s.cat.categories.to_list()) #['하', '중', '상', '최상']

# cat.remove_unused_categories()
pp(s.cat.categories)
# '최상' 이라는 카테고리는 데이터가 없으므로 카테고리로서의 의미가 없으므로 제거
s = s.cat.remove_unused_categories()
pp(s.cat.categories)
pp(type(s))  # <class 'pandas.Series'>

# cat.reorder_categories()
order = ['하','중','상'] # 새로운 카테고리(범주)로 사용할 리스트
# 범주의 순서를 다시 지정할 때는 기존 범주를 반드시 포함 해야함
s = s.cat.reorder_categories(order,ordered=True) # 순서 있는 케테고리로 재구성
pp(s.cat.categories) # Index(['하', '중', '상'], dtype='str')
pp(type(s.cat.categories)) #<class 'pandas.Index'>
pp(s.cat.ordered) # 순서 있음 #True
pp(s.sort_values()) # 순서가 있어야 정렬이 가능
pp(s.cat.codes) #  하 > 0 , 중 > 1, 상 > 2 (순서에 대한 번호가 내부적으로 설정됨)

data = pd.Series([1,2,3,4,5,6,7,8,9,100])

# pd.cut()
# - 값의 범위를 기준으로 구간을 나눔,
# - 각 구간에 포함되는 데이터 개수는 다를 수 있음
cut_result = pd.cut(
    data,
    bins=2,
    labels=['낮은구간','높은구간']
)
pp(pd.DataFrame({'값': data, 'cut 결과': cut_result}))
pp(cut_result.value_counts(sort=False))

# pd.qcut()
# - 데이터 개수 또는 분위수(quantile)를 기준으로 구간을 나누고
# - 각 구간에 들어가는 데이터 수는 가능한 비슷 하게 자른다
qcut_result = pd.qcut(
    data,
    q=2,
    labels=['하위 50%', '상위 50%']
)
# 하위 50% 5개 상위50% 5개
pp(pd.DataFrame({'값': data, 'cut 결과': qcut_result}))
pp(qcut_result.value_counts(sort=False))













