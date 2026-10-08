# day28_application.py
# 주제:day28 Application 과제 - 온라인 쇼핑 주문 대시보드

# [목표]
# 사용자 선택 조건에 따라 데이터를 필터링하고 Metric과 차트를 갱신하는 대시보드를 작성합니다.

# [데이터]
# 코드에서 다음 컬럼을 가진 샘플 DataFrame을 직접 생성합니다.
# 주문일
# 카테고리
# 주문금액
# 주문수량

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt


from include.graph_config import set_graph

set_graph(10,8,13)

# 카테고리는 최소 4개를 사용합니다.
df = pd.DataFrame(
    {
        "주문일": pd.date_range(
            "2026-09-01",
            periods=12,
            freq="D"
        ),
        "카테고리": [
            "전자기기",
            "식품",
            "도서",
            "생활",
            "전자기기",
            "식품",
            "도서",
            "생활",
            "전자기기",
            "식품",
            "도서",
            "생활"
        ],
        "주문금액": [
            120000,
            35000,
            28000,
            54000,
            85000,
            42000,
            31000,
            67000,
            210000,
            29000,
            45000,
            72000
        ],
        "주문수량": [
            1, 3, 2, 2, 1, 4,
            2, 3, 1, 2, 3, 2
        ]
    }
)

st.set_page_config(
    page_title='온라인 쇼핑 주문 대시보드',
    layout="wide"
)

st.title('온라인 쇼핑 주문 대시보드')
with st.sidebar:
    categories = ['전체'] + sorted(df['카테고리'].unique().tolist())
    category = st.selectbox('카테고리', categories)

filtered = df.copy()
if category != '전체':
    filtered = filtered[['카테고리'] == category]

c1, c2, c3 = st.columns(3)
c1.metric('주문건수',len(filtered))
c2.metric('총 주문금액', f"{filtered['주문금액'].sum():,}원")
c3.metric('총 주문수량', f"{filtered['주문수량'].sum():,}개")

st. subheader('주문 목록')

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)


st.subheader('카테고리 별 총 주문 금액')

summary = (
    filtered.groupby('카테고리')['주문금액'].sum().sort_values(ascending=False)
)

fig, ax = plt.subplots()
ax.bar(summary.index, summary.values, align='center')
ax.set_title('카테고리별 총 주문금액')
ax.set_xlabel('카테고리')
ax.set_ylabel('주문금액')
st.pyplot(fig)
plt.close(fig)









































