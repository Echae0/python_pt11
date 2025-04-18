import streamlit as st
import pandas as pd
from dotenv import load_dotenv
# streamlit run streamlit_pt11_prec.py
import os
import numpy as np

# model = joblib.load("survival_predictor.pkl")

# # UI
# st.title("📈 심정지 생존률 예측기")

# year = st.number_input("예측할 연도 (예: 2025)", min_value=2020, max_value=2100, value=2025)

# if st.button("예측하기"):
#     prediction = model.predict(np.array([[year]]))
#     st.success(f"📊 {year}년 예상 생존률은 {prediction[0]:.2f}% 입니다.")