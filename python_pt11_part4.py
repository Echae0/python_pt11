# %% [markdown]
# #### 머신러닝 모델 생성 및 비교
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
from python_pt11_part2 import final_heart_df

# %%
# RandomForest Model
x = final_heart_df[['전체 발생률', '전체 뇌기능 회복률', '병원 합계']]
y = final_heart_df['전체 생존율']

# 데이터 분할
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 모델 학습
model = RandomForestRegressor(random_state=42)
model.fit(x_train, y_train)

# 예측 및 평가
y_pred = model.predict(x_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
print(f"R²: {r2:.3f}")
print(f'Mean Squared Error: {mse:.3f}')

# %%
# RandomForest 모델 교차검증
scores = cross_val_score(model, x, y, cv=5, scoring='r2')
print(scores)
print(f'R² 평균: {scores.mean():.3f}, 표준편차: {scores.std():.3f}')

# %%
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

# %%
# Gradient Boosting 모델 교차검증
scores2 = cross_val_score(gb_model, x, y, cv=5, scoring='r2')
print(scores2)
print(f'R² 평균: {scores2.mean():.3f}, 표준편차: {scores2.std():.3f}')

# %%
sample_row = final_heart_df[final_heart_df['시도'] == '서울']
predicted_data = sample_row[['연도', '시도', '전체 생존율', '전체 발생률', '전체 뇌기능 회복률', '병원 합계']]
predicted_data

# %%
new_data = pd.DataFrame({
    '전체 발생률': [47.3],
    '전체 뇌기능 회복률': [7.2],
    '병원 합계': [286]
})

# Random Forest Model 예측
predicted_survival = model.predict(new_data)
print(f"예측된 전체 생존율: {predicted_survival[0]:.2f}")

# %%
# Gradient Boosting Model 예측
predicted_survival = gb_model.predict(new_data)
print(f"예측된 전체 생존율: {predicted_survival[0]:.2f}")

# %%

x = final_heart_df[['연도']] 
y = final_heart_df['전체 생존율']  

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)

# 평가
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.3f}")
r2 = r2_score(y_test, y_pred)
print(f"R²: {r2:.3f}")


# %%
new_data = pd.DataFrame({'연도': [2020]})
predicted_value = model.predict(new_data)

print(f"2020년의 예측된 전체 생존율: {predicted_value[0]:.2f}")