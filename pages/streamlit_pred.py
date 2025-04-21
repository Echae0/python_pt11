# 📈 심정지 생존률 예측기

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
# streamlit run streamlit_pred_test.py
import os
import numpy as np
from python_pt11_part4 import predict_survival_rate, rf_model, gb_model, importance, plot

# UI
st.title("📈 심정지 생존률 예측기")

occur_rate_input = st.text_input("전체 발생률 (예: 47.3)")
brain_heal_rate_input = st.text_input("뇌기능 회복률 (예: 7.2)")
hospital_count_input = st.text_input("병원 수 (예: 286)")

feature_importance_list = importance()
importance_dict = {feature: round(importance * 100,2) for feature, importance in feature_importance_list}
df = pd.DataFrame([list(importance_dict.keys()), list(importance_dict.values())])
df = pd.DataFrame.from_dict(
    {"중요도 (%)": importance_dict},
    orient='index',
    columns=["전체 발생률", "전체 뇌기능 회복률", "병원 합계"]
)
df.index.name = "특성"

if st.button("예측하기"):
    if occur_rate_input and brain_heal_rate_input and hospital_count_input:
        try:
            # 입력값을 float로 변환
            occur_rate = float(occur_rate_input)
            brain_heal_rate = float(brain_heal_rate_input)
            hospital_count = float(hospital_count_input)

            # 입력값 확인
            st.write("🧾 입력값 확인")
            st.write(f"전체 발생률: {occur_rate}")
            st.write(f"뇌기능 회복률: {brain_heal_rate}")
            st.write(f"병원 수: {hospital_count}")

            # 예측 함수 호출
            result = predict_survival_rate(occur_rate, brain_heal_rate, hospital_count)

            if result is not None and isinstance(result, tuple) and len(result) == 2:
                pred_rf, pred_gb = result
                st.table(df)
                st.success("✅ 예측 완료!")
                st.write(f"🌲 Random Forest 예측 생존율: **{pred_rf:.2f}%**")
                st.write(f"🔥 Gradient Boosting 예측 생존율: **{pred_gb:.2f}%**")
                plot()
            else:
                st.error("예측을 할 수 없습니다. 모델 함수가 올바른 값을 반환하지 않았습니다.")
        except ValueError:
            st.error("❌ 숫자를 정확히 입력해주세요 (소수점 포함 가능)")
    else:
        st.warning("⚠️ 모든 값을 입력해주세요.")
