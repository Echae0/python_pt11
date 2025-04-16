import streamlit as st
import pandas as pd

st.title("급성심장정지 위험도 파악 및 현황분석")

region_name = st.text_input('조회할 지역이름과 연도를 선택해주세요 (예 : 경기, 인천)')
button_clicked = st.button("조회")    