# %% [markdown]
# ### 파이썬 미니 프로젝트 11조

# %%
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# %%
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# %%
[ (font.name, font.fname) for font in fm.fontManager.ttflist if 'Mal' in font.name ]

font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path).get_name()

matplotlib.rc('font', family=font_prop)

# %% [markdown]
# #### 1. 데이터 수집

# %%
# url과 파라미터 설정 + 결과 확인
url = 'http://apis.data.go.kr/1352000/ODMS_STAT_09/callStat09Api'
key = os.getenv("SERVICE_KEY")
params ={'serviceKey' : f'{key}', 'apiType' : 'JSON'}

response = requests.get(url, params=params)
print(response.content)

# 서버의 응답 상태 출력
print(response.status_code) 

# %%
def api_df(num):
    
    url = f'http://apis.data.go.kr/1352000/ODMS_STAT_{num}/callStat{num}Api'
    key = os.getenv("SERVICE_KEY")
    params ={'serviceKey' : f'{key}', 
             'apiType' : 'JSON'}

    response = requests.get(url, params=params)
    # 응답 상태가 정상인 경우 (200)에 데이터프레임 반환
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['items'])
        return df
    else:
        print(f"오류 발생: {response.status_code}")

# %%
# 급성심장정지 발생률
heart_occur_eng = api_df('08')

# 급성심장정지 생존율
heart_live_eng = api_df('09')

# 급성심장정지 뇌기능 회복률
heart_heal_eng = api_df('10')

# %%
# 전국 병원 데이터 csv 파일 불러오기
hospital_df_eng = pd.read_csv("보건복지부_병원 및 의원 수_의료기관 종류별_시도별_20221231.csv", encoding='cp949')

# %% [markdown]
# #### 2. 데이터 전처리

# %%
# 급성심장정지 데이터프레임의 연도, 지역 컬럼을 앞으로 불러오기
# 알아보기 힘든 컬럼 이름 수정

front_cols = ['year', 'dvsd']
heart_occur_eng = heart_occur_eng[front_cols + [col for col in heart_occur_eng.columns if col not in front_cols]]

heart_occur = heart_occur_eng.rename(columns={
    'year': '연도',
    'dvsd': '시도',
    'allStdrOcrt': '전체 표준화 발생률',
    'othdsOcrt': '질병외 발생률',
    'dsStdrOcrt': '질병 표준화 발생률',
    'allOcrt': '전체 발생률',
    'allOccr': '전체 발생',
    'dsOcrt': '질병 발생률',
    'dsOccr': '질병 발생',
    'othdsStdrOcrt': '질병외 표준화 발생률',
    'othdsOccr': '질병외 발생'
})

ordered_occur = [
    '연도', '시도',
    '전체 발생', '전체 발생률', '전체 표준화 발생률',
    '질병 발생', '질병 발생률', '질병 표준화 발생률',
    '질병외 발생', '질병외 발생률', '질병외 표준화 발생률'
]

# 데이터타입 object에서 float나 int형식으로 변경
heart_occur = heart_occur[ordered_occur]
heart_occur = heart_occur.sort_values(by='연도').reset_index(drop=True)
heart_occur[heart_occur.columns.difference(['시도'])] = heart_occur[heart_occur.columns.difference(['시도'])].apply(pd.to_numeric, errors='coerce')

heart_occur.head()

# %%
heart_live_eng = heart_live_eng[front_cols + [col for col in heart_live_eng.columns if col not in front_cols]]

heart_live = heart_live_eng.rename(columns={
    'year': '연도',
    'dvsd': '시도',
    'dsStdrSrvrt': '질병 표준화 생존률',
    'allSvr': '전체 생존',
    'allStdrSrvrt': '전체 표준화 생존률',
    'dsSvr': '질병 생존',
    'othdsStdrSrvrt': '질병외 표준화 생존률',
    'dsSrvrt': '질병 생존율',
    'othdsSvr': '질병외 생존',
    'allSrvrt': '전체 생존율',
    'othdsSrvrt': '질병외 생존율'
})

ordered_live = [
    '연도', '시도',
    '전체 생존', '전체 생존율', '전체 표준화 생존률',
    '질병 생존', '질병 생존율', '질병 표준화 생존률',
    '질병외 생존', '질병외 생존율', '질병외 표준화 생존률'
]

# 데이터타입 object에서 float나 int형식으로 변경
heart_live = heart_live[ordered_live]
heart_live = heart_live.sort_values(by='연도').reset_index(drop=True)
heart_live[heart_live.columns.difference(['시도'])] = heart_live[heart_live.columns.difference(['시도'])].apply(pd.to_numeric, errors='coerce')

heart_live.head()

# %%
heart_heal_eng = heart_heal_eng[front_cols + [col for col in heart_heal_eng.columns if col not in front_cols]]

heart_heal = heart_heal_eng.rename(columns={
    'year': '연도',
    'dvsd': '시도',
    'allStbfnRcvr': '전체 표준화 뇌기능 회복률',
    'othdsStbfnRcvr': '질병외 표준화 뇌기능 회복률',
    'dsBrfr': '질병 뇌기능 회복',
    'allBrfr': '전체 뇌기능 회복',
    'dsBrfrr': '질병 뇌기능 회복률',
    'allBrfcRcvr': '전체 뇌기능 회복률',
    'dsStbfnRcvr': '질병 표준화 뇌기능 회복률',
    'othdsBrfr': '질병외 뇌기능 회복',
    'othdsBrfcRcvr': '질병외 뇌기능 회복률'
})

ordered_heal = [
    '연도', '시도',
    '전체 뇌기능 회복', '전체 뇌기능 회복률', '전체 표준화 뇌기능 회복률',
    '질병 뇌기능 회복', '질병 뇌기능 회복률', '질병 표준화 뇌기능 회복률',
    '질병외 뇌기능 회복', '질병외 뇌기능 회복률', '질병외 표준화 뇌기능 회복률'
]

# 데이터타입 object에서 float나 int형식으로 변경
heart_heal = heart_heal[ordered_heal]
heart_heal = heart_heal.sort_values(by='연도').reset_index(drop=True)
heart_heal[heart_heal.columns.difference(['시도'])] = heart_heal[heart_heal.columns.difference(['시도'])].apply(pd.to_numeric, errors='coerce')

heart_heal.head()

# %%
# 병원 데이터 필요한 컬럼만 남기기 (연도, 시도, 종합병원, 일반병원)
hospital_df = hospital_df_eng[['연도', '시도', '병의원_종합병원', '병의원_일반병원']]

# %%
# 컬럼이름 수정
hospital_df = hospital_df.rename(columns={
    '병의원_종합병원': '종합병원',
    '병의원_일반병원': '일반병원'
})

hospital_df

# %%
# 컬럼이름 수정
hospital_df = hospital_df.rename(columns={
    '병의원_종합병원': '종합병원',
    '병의원_일반병원': '일반병원'
})

hospital_df

# %%
# 시도 컬럼의 데이터 내용 수정 (ex. 서울 Seoul -> 서울)
hospital_df['시도'] = hospital_df['시도'].str[:2]

# 급성심장정지 데이터와 데이터 추출 연도 일치를 위해 2016-2019년도 데이터 추출
hospital_df = hospital_df[hospital_df['연도'].between(2016,2019)].reset_index(drop=True)

hospital_df

# %%
# 전체 데이터 합치기
final_heart_df = heart_live.merge(heart_heal, on=['연도', '시도'], how='left').\
    merge(heart_occur, on=['연도', '시도'], how='left').\
    merge(hospital_df, on=['연도', '시도'], how='left')
    
# 전체 병원 개수 컬럼 생성
final_heart_df['병원 합계'] = final_heart_df['종합병원'] + final_heart_df['일반병원']
final_heart_df.head()

# %% [markdown]
# #### 3. 데이터 분석 (EDA & 상관관계 분석)

# %% [markdown]
# 데이터 파악

# %%
final_heart_df.info()
final_heart_df.describe()

# %% [markdown]
# 상관관계

# %%
# 급성심정지 생존율과 뇌기능 회복률의 상관관계 확인
correlation1 = final_heart_df[['전체 생존율', '전체 뇌기능 회복률']].corr().iloc[0, 1]
print(f"급성심장정지 생존율과 뇌기능 회복률의 상관계수: {correlation1:.3f}")

# %%
plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='전체 뇌기능 회복률', y='전체 생존율')
plt.title(f'전체 생존율 vs 뇌기능 회복률 (상관계수: {correlation1:.3f})', fontsize=16)
plt.xlabel('전체 뇌기능 회복률 (%)', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.show()

# %%
# 급성심정지 생존율과 발생률의 상관관계 확인
correlation2 = final_heart_df[['전체 생존율', '전체 발생률']].corr().iloc[0, 1]
print(f"급성심장정지 생존율과 발생률의 상관계수: {correlation2:.3f}")

# %%
plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='전체 발생률', y='전체 생존율')
plt.title(f'전체 생존율 vs 전체 발생률 (상관계수: {correlation2:.3f})', fontsize=16)
plt.xlabel('전체 발생률 (%)', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.show()

# %%
# 병원 개수와 생존율의 상관관계 확인
correlation3 = final_heart_df[['병원 합계', '전체 생존율']].corr().iloc[0, 1]
print(f"병원합계와 생존율의 상관계수: {correlation3:.3f}")

# %%
plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='병원 합계', y='전체 생존율')
plt.title(f'병원 합계 vs 전체 발생률 (상관계수: {correlation3:.3f})', fontsize=16)
plt.xlabel('병원 합계', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.show()

# %%
# 병원 개수와 뇌기능 회복률의 상관관계 확인
correlation4 = final_heart_df[['병원 합계', '전체 뇌기능 회복률']].corr().iloc[0, 1]
print(f"병원합계와 뇌기능 회복률의 상관계수: {correlation4:.3f}")

# %%
plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='병원 합계', y='전체 뇌기능 회복률')
plt.title(f'병원 합계 vs 전체 뇌기능 회복률 (상관계수: {correlation4:.3f})', fontsize=16)
plt.xlabel('병원 합계', fontsize=12)
plt.ylabel('전체 뇌기능 회복률', fontsize=12)
plt.show()

# %% [markdown]
# #### 탐색적 데이터 분석 + 시각화

# %%
heart_occur_melted = heart_occur.melt(id_vars=['연도', '시도'], 
                                      value_vars=['전체 발생률'],
                                      var_name='변수', value_name='값')

plt.figure(figsize=(15, 5))
sns.barplot(data=heart_occur_melted, x='시도', y='값', hue='연도', palette=['#FF6F61', '#4A90E2', '#7ED321', '#FBC02D'])

plt.title('연도 및 시도별 급성심장정지 전체 발생률', fontsize=20)
plt.xlabel('시도', fontsize=12)
plt.ylabel('전체 발생률', fontsize=12)
plt.xticks(rotation=45)  

plt.legend()
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(15, 7))

palette = {
    '서울': '#E6194B', '부산': '#3CB44B', '대구': '#FFE119', '인천': '#0082C8', '광주': '#F58231',
    '대전': '#911EB4', '울산': '#46F0F0', '세종': '#F032E6', '경기': '#D2F53C', '강원': '#FABEBE',
    '충북': '#008080', '충남': '#E6BEFF', '전북': '#AA6E28', '전남': '#800000', '경북': '#000000',
    '경남': '#A9A9A9', '제주': '#FFD700'
}

sns.lineplot(data=heart_occur_melted, x='연도', y='값', hue='시도', marker='o', palette= palette)

plt.title('연도 및 시도별 급성심장정지 전체 발생률 추세 (2016-2019)', fontsize=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('전체 발생률 (%)', fontsize=12)
plt.xticks([2016, 2017, 2018, 2019])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
heart_live_melted = heart_live.melt(id_vars=['연도', '시도'], 
                                      value_vars=['전체 생존율'],
                                      var_name='변수', value_name='값')

plt.figure(figsize=(15, 6))
sns.barplot(data=heart_live_melted, x='시도', y='값', hue='연도', palette=['#FF6F61', '#4A90E2', '#7ED321', '#FBC02D'])

plt.title('연도 및 시도별 급성심장정지 전체 생존률', fontsize=20)
plt.xlabel('시도', fontsize=12)
plt.ylabel('전체 생존율', fontsize=12)
plt.xticks(rotation=45)  

plt.legend()
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(15, 7))

palette = {
    '서울': '#E6194B', '부산': '#3CB44B', '대구': '#FFE119', '인천': '#0082C8', '광주': '#F58231',
    '대전': '#911EB4', '울산': '#46F0F0', '세종': '#F032E6', '경기': '#D2F53C', '강원': '#FABEBE',
    '충북': '#008080', '충남': '#E6BEFF', '전북': '#AA6E28', '전남': '#800000', '경북': '#000000',
    '경남': '#A9A9A9', '제주': '#FFD700'
}

sns.lineplot(data=heart_live_melted, x='연도', y='값', hue='시도', marker='o', palette= palette)

plt.title('연도 및 시도별 급성심장정지 전체 생존율 추세 (2016-2019)', fontsize=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.xticks([2016, 2017, 2018, 2019])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# %%
heart_heal_melted = heart_heal.melt(id_vars=['연도', '시도'], 
                                      value_vars=['전체 뇌기능 회복률'],
                                      var_name='변수', value_name='값')

plt.figure(figsize=(15, 6))
sns.barplot(data=heart_heal_melted, x='시도', y='값', hue='연도', palette=['#FF6F61', '#4A90E2', '#7ED321', '#FBC02D'])

plt.title('연도 및 시도별 급성심장정지 전체 뇌기능 회복률', fontsize=20)
plt.xlabel('시도', fontsize=12)
plt.ylabel('전체 뇌기능 회복률', fontsize=12)
plt.xticks(rotation=45)  

plt.legend()
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(15, 7))

palette = {
    '서울': '#E6194B', '부산': '#3CB44B', '대구': '#FFE119', '인천': '#0082C8', '광주': '#F58231',
    '대전': '#911EB4', '울산': '#46F0F0', '세종': '#F032E6', '경기': '#D2F53C', '강원': '#FABEBE',
    '충북': '#008080', '충남': '#E6BEFF', '전북': '#AA6E28', '전남': '#800000', '경북': '#000000',
    '경남': '#A9A9A9', '제주': '#FFD700'
}

sns.lineplot(data=heart_heal_melted, x='연도', y='값', hue='시도', marker='o', palette= palette)

plt.title('연도 및 시도별 급성심장정지 전체 뇌기능 회복률 추세 (2016-2019)', fontsize=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('전체 뇌기능 회복률 (%)', fontsize=12)
plt.xticks([2016, 2017, 2018, 2019])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# %%
mean_df = final_heart_df.groupby('시도')['병원 합계'].mean().reset_index()

region_colors = {
    '서울': '#E6194B', '부산': '#3CB44B', '대구': '#FFE119', '인천': '#0082C8', '광주': '#F58231',
    '대전': '#911EB4', '울산': '#46F0F0', '세종': '#F032E6', '경기': '#D2F53C', '강원': '#FABEBE',
    '충북': '#008080', '충남': '#E6BEFF', '전북': '#AA6E28', '전남': '#800000', '경북': '#000000',
    '경남': '#A9A9A9', '제주': '#FFD700'
}
colors = [region_colors[sido] for sido in mean_df['시도']]

# 한글 깨짐 방지 (폰트 설정)
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows인 경우
# plt.rcParams['font.family'] = 'AppleGothic'  # macOS인 경우
plt.rcParams['axes.unicode_minus'] = False

# 시도별 병원 평균 막대그래프
plt.figure(figsize=(12, 6))
bars = plt.bar(mean_df['시도'], mean_df['병원 합계'], color=colors)

plt.title('연도별 평균 지역별 병원 수', fontsize=14)
plt.xlabel('시도', fontsize=12)
plt.ylabel('병원 수 평균', fontsize=12)

# 값 라벨 위에 표시
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.0f}', ha='center', va='bottom', fontsize=10)

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# #### 머신러닝 모델 생성 및 비교

# %%
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor

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


