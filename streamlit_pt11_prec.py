import streamlit as st
import pandas as pd
from dotenv import load_dotenv
# streamlit run streamlit_pt11_prec.py
import os
import numpy as np
from python_pt11_part4 import predict_survival_rate, rf_model, gb_model

# UI
st.title("📈 심정지 생존률 예측기")

occur_rate_input = st.text_input("전체 발생률 (예: 2025)")
brain_heal_rate_input = st.text_input("뇌기능 회복률 (예: 2025)")
hospital_count_input = st.text_input("병원 수 (예: 2025)")

if st.button("예측하기"):
    if occur_rate_input and brain_heal_rate_input and hospital_count_input:
        try:
            # 입력값을 float로 변환
            occur_rate = float(occur_rate_input)
            brain_heal_rate = float(brain_heal_rate_input)
            hospital_count = float(hospital_count_input)

            # 예측 함수 호출
            pred_rf, pred_gb = predict_survival_rate(occur_rate, brain_heal_rate, hospital_count)
            
            if pred_rf is not None and pred_gb is not None:
                # 예측 결과 출력
                st.write(f"Random Forest 예측 생존율: {pred_rf:.2f}%")
                st.write(f"Gradient Boosting 예측 생존율: {pred_gb:.2f}%")
                
            else:
                st.error("예측을 할 수 없습니다. 모델에 문제가 있을 수 있습니다.")
        except ValueError:
            st.error("숫자를 정확히 입력해주세요 (소수점 포함 가능)")
    else:
        st.warning("모든 값을 입력해주세요.")
        