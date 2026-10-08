# day14_ex2.py
# 주제 : plotly 인터렉티브 시각화, folium 지도 사각형


'''
* plotly
    - 웹기반 인터렉티브 데이터 시각화 라이브러리
    - 마우스를 올리면 데이터 값을 확인 할 수 있음
    - 확대, 축소, 이동, 범례 선택, 이미지 저장 ... 기능 제공
    - plotly.express 를 주요 사용

* folium
    - 위도/경도 를 이용한 지도 시각화 라이브러리
    - Marker를 사용하여 지도에 데이터 위치 표시
    - 결과를 HTML 파일로 저장하여 웹브라우져에서 확인하거나 웹서비스 가능
'''

# 설치 : Alt + F12 > pip install plotly folium



import pandas as pd
from pathlib import Path # 경로 처리
import plotly.express as px
import folium
import webbrowser

from matplotlib.pyplot import title

# 결과를 저장 폴더
output_dir = Path('day14_output')
output_dir.mkdir(exist_ok=True)
df = pd.DataFrame({
    "월": ["1월", "2월", "3월", "4월", "5월", "6월"],
    "광고비": [100, 120, 130, 150, 170, 200],
    "방문자수": [3000, 3500, 3800, 4200, 4700, 5300],
    "매출": [250, 290, 310, 360, 410, 480]
})

# poltly 선그래프
# fig = px.line(
#     df,
#     x = '월',
#     y = '매출',
#     markers=True,
#     title='월별 매출 추세'
# )
# fig.show()

# plotly 막대 그래프
# fig = px.bar(
#     df,
#     x = '월',
#     y = '매출',
#     text= '매출', # 막대에 값 표시
#     title='월별 매출'
# )
# fig.show()

# plotly
# fig = px.scatter(
#     df,
#     x = '광고비',
#     y = '매출',
#     size= '방문자수', # 점 크기 기준
#     hover_data=['월'], #마우스 오버시 표시할 컬럼
#     title ='광고비와 매출의 관계'
# )
# fig.show()

# folium 지도 시각화

# # folium Map 생성
# m = folium.Map(
#     location= [37.5665,126.9780], # 맵의 중심 위경도 (서울 시청 위/경도)
#     zoom_start=12, # 최초 로딩시 줌의 확대 레벨
# )
# map_file = output_dir / "map.html" # 맵을 HTML로 저장할때 파일명
# m.save(map_file) # 맵을 HRML 로 저장
#
# # 맵의 절대경롤를 URI변환 해서 웹브라우져 에서 오픈
# webbrowser.open(map_file.resolve().as_uri())

# folium Maker : 맵에 마커 표시
m = folium.Map(
    location= [37.55,126.98], # 맵의 중심 위경도 (서울 시청 위/경도)
    zoom_start=11, # 최초 로딩시 줌의 확대 레벨
)
# 지명, 위도, 경도 리스트
location = [
    ['서울시청',37.5665,126.9780],
    ['감남역',37.4979,127.0276],
    ['홍대입구',37.5672,126.9254],
    ['우리집',37.544,126.865],
]
for name, lat, lon in location:
    folium.Marker(
        location=[lat, lon], # 마커 위경도
        tooltip= name, # 마우스를 올렸을떄 보여줄 텍스트
        popup= name + '클릭함!', # 마우스 클릭 했을때 보여줄 텍스트
    ).add_to(m) # 마커를 맵에 추가

map_file = output_dir/'marker_map.html'
m.save(output_dir/'marker_map.html')
webbrowser.open(map_file.resolve().as_uri())






