# day27_basic.py
import streamlit as st

st.title('교육과정 상담 신청')

name = st.text_input(
    '이름',
    placeholder='입력'
)

course = st.selectbox(
    '희망 과정',
    ['파이썬','데이터분석','에이아이']
)

consult_time = st.radio(
    '상담 희망 시간',
    ['오전','오후','저녁']
)

if st.button('신청'):
    if not name.strip():
        st.warning('이름 다시 입력')
    else:
        st.success('상담 신청 접수 완료')
        st.write('이름',name)
        st.write('희망 과정',course)
        st.write('상담 시간',consult_time)


















