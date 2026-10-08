# day28_challenge.py
# 주제: day28 Challenge 과제 - 운동 기록·음성 메모 대시보드
#
# [목표]
# 데이터 시각화와 WAV 파일 기능을 Tabs로 통합하여 서로 다른 형식의 데이터를 하나의 웹서비스에 구성합니다.
from pathlib import Path
import numpy as np
import streamlit as st
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

from include.graph_config import set_graph

set_graph(18,12,8)
df = pd.DataFrame(
    {
        "날짜": pd.date_range(
            "2026-09-01",
            periods=10,
            freq="D"
        ),
        "운동종류": [
            "걷기",
            "달리기",
            "자전거",
            "걷기",
            "달리기",
            "자전거",
            "걷기",
            "달리기",
            "자전거",
            "걷기"
        ],
        "운동시간": [
            40, 30, 60, 50, 35,
            70, 45, 25, 55, 60
        ],
        "소모칼로리": [
            160, 280, 420, 200, 320,
            490, 180, 240, 390, 230
        ]
    }
)
st.header('운동 기록·음성 메모 대시보드')
filtered_sports = df.copy()



def hab(Serise):
    total = 0
    for i in Serise:
        total += i
    return total

# [구성]
tab1, tab2 = st.tabs(['운동기록','음성기록'])

# 첫 번째 탭: 운동 기록
with tab1:
    if '운동종류' in df.columns:
        sports = df['운동종류'].dropna().astype(str).unique().tolist()
        sports = ['전체'] + sorted(sports)
        sport = st.selectbox('운동종류 선택', sports)

    else:
        sport = '전체'
        st.caption('운동종류 컬럼이 없어서 필터 생략')

    # 운동종류를 선택해 데이터를 필터링합니다.
    if sport != '전체' and '운동종류' in filtered_sports.columns:
        filtered_sports = filtered_sports[
            filtered_sports['운동종류'].astype(str) == sport
        ]

    if filtered_sports.empty:
        st.warning('조건에 맞는 데이터 없음')

    else:
        st.subheader('운동기록')

        # Metric 3개: 기록 건수, 총 운동시간, 총 소모칼로리
        c1, c2, c3 = st.columns([1, 1, 1])

        c1.metric('기록 건수', len(filtered_sports))
        c2.metric('총 운동시간', hab(filtered_sports['운동시간']))
        c3.metric('총 소모칼로리', hab(filtered_sports['소모칼로리']))

        # 날짜별 소모칼로리를 선 그래프로 출력합니다.
        sports_line_data = (filtered_sports.groupby('날짜')['소모칼로리'].sum())

        fig, ax = plt.subplots()

        ax.plot(sports_line_data.index,sports_line_data.values)
        ax.set_title('날짜별 소모칼로리')
        ax.set_xlabel('날짜')
        ax.set_ylabel('소모칼로리')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
        # 필터링된 DataFrame을 출력합니다.
        st.dataframe(filtered_sports,use_container_width=True)

# 두 번째 탭: 음성 메모
with tab2:
    st.subheader('음성메모')

    # WAV 파일만 업로드할 수 있도록 합니다.
    wav_file = st.file_uploader('WAV 파일 선택',type=['wav'])

    # WAV가 없을 때는 안내 메시지를 표시합니다.
    if wav_file is None:
        st.info('WAV 파일을 업로드해주세요.')
    else:
        # 업로드된 파일명과 크기를 표시합니다.
        file_name = wav_file.name
        file_size = len(wav_file.getvalue())
        c1, c2 = st.columns(2)
        c1.metric('파일명',file_name)
        c2.metric('파일 크기',f'{file_size:,} bytes')

        # st.audio()로 음성을 재생합니다.
        st.audio(wav_file,format='audio/wav')