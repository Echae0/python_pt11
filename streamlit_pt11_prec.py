import streamlit as st
import pandas as pd
from dotenv import load_dotenv
# streamlit run streamlit_pt11_prec.py
import os
import numpy as np
from python_pt11 import predicted_survival, predicted_value, model
# UI
st.title("📈 심정지 생존률 예측기")

year = st.number_input("예측할 연도 (예: 2025)", min_value=2020, max_value=2100, value=2025)

new_data = pd.DataFrame({'연도': [year]})


print(f"2020년의 예측된 전체 생존율: {predicted_value[0]:.2f}")

if st.button("예측하기"):
    predicted_value = model.predict(new_data)
    st.success(f"📊 {year}년 예상 생존률은 {predicted_value[0]:.2f}% 입니다.")