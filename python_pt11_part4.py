from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import streamlit as st

final_heart_df = pd.read_csv('final_heart_df.csv', encoding='utf-8-sig')
# RandomForest Model
x = final_heart_df[['전체 발생률', '전체 뇌기능 회복률', '병원 합계']]
y = final_heart_df['전체 생존율']

# 데이터 분할
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 모델 학습
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(x_train, y_train)

# 예측 및 평가
y_pred = rf_model.predict(x_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"R²: {r2:.3f}")
print(f'Mean Squared Error: {mse:.3f}')

# RandomForest 모델 교차검증
scores = cross_val_score(rf_model, x, y, cv=5, scoring='r2')
print(scores)
print(f'R² 평균: {scores.mean():.3f}, 표준편차: {scores.std():.3f}')

# Gradient Boosting Model

# 모델 학습
gb_model = GradientBoostingRegressor(random_state=42)
gb_model.fit(x_train, y_train)


# 예측 및 평가
gb_pred = gb_model.predict(x_test)
gb_mse = mean_squared_error(y_test, gb_pred)
gb_r2 = r2_score(y_test, gb_pred)


print(f"R²: {gb_r2:.3f}")
print(f"Mean Squared Error: {gb_mse:.3f}")

# Gradient Boosting 모델 교차검증
scores2 = cross_val_score(gb_model, x, y, cv=5, scoring='r2')
print(scores2)
print(f'R² 평균: {scores2.mean():.3f}, 표준편차: {scores2.std():.3f}')

sample_row = final_heart_df[final_heart_df['시도'] == '서울']
predicted_data = sample_row[['연도', '시도', '전체 생존율', '전체 발생률', '전체 뇌기능 회복률', '병원 합계']]
predicted_data

predict_df = pd.DataFrame({
    '전체 발생률': [47.3],
    '전체 뇌기능 회복률': [7.2],
    '병원 합계': [286]
})

# Random Forest Model 예측
predicted_survival = rf_model.predict(predict_df)
print(f"예측된 전체 생존율 (Random Forest Model): {predicted_survival[0]:.2f}")

# Gradient Boosting Model 예측
predicted_survival = gb_model.predict(predict_df)
print(f"예측된 전체 생존율 (Gradient Boosting Model): {predicted_survival[0]:.2f}")

def predict_survival_rate(occur_rate, brain_heal_rate, hospital_count):
    predict_df = pd.DataFrame({
        '전체 발생률': [occur_rate],
        '전체 뇌기능 회복률': [brain_heal_rate],
        '병원 합계': [hospital_count] })
    
    print(predict_df)
    
    pred_rf = rf_model.predict(predict_df)[0]
    pred_gb = gb_model.predict(predict_df)[0]
    
    print(f"입력 받은 전체 발생률: {occur_rate}")
    print(f"입력 받은 전체 뇌기능 회복률: {brain_heal_rate}")
    print(f"입력 받은 병원 합계: {hospital_count}")
    print("--------------------------")
    print(f"Random Forest 예측 생존율: {pred_rf:.2f}%")
    print(f"Gradient Boosting 예측 생존율: {pred_gb:.2f}%")
    return pred_rf, pred_gb

def importance():
    importances = rf_model.feature_importances_
    features = ['전체 발생률', '전체 뇌기능 회복률', '병원 합계']
    return list(zip(features, importances))
        
def plot():
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(rf_model.estimators_[0], 
              feature_names=['전체 발생률', '전체 뇌기능 회복률', '병원 합계'],
              filled=True,
              rounded=True,
              fontsize=10,
              ax=ax)  # ax 매개변수 추가
    ax.set_title("랜덤포레스트 내 개별 결정트리 시각화")
    
    # Streamlit에 출력
    st.pyplot(fig)

predict_survival_rate(47.3, 7.2, 286)
    
predict_survival_rate(53.6, 5.2, 121)