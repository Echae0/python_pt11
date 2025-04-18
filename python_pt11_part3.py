import requests
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns


final_heart_df = pd.read_csv('final_heart_df.csv', encoding='utf-8-sig')
heart_occur = pd.read_csv('heart_occur.csv', encoding='utf-8-sig')
heart_live = pd.read_csv('heart_live.csv', encoding='utf-8-sig')
heart_heal = pd.read_csv('heart_heal.csv', encoding='utf-8-sig')

[ (font.name, font.fname) for font in fm.fontManager.ttflist if 'Mal' in font.name ]

font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_prop = fm.FontProperties(fname=font_path).get_name()
matplotlib.rc('font', family=font_prop)

palette = {
    '서울': '#E6194B', '부산': '#3CB44B', '대구': '#FFE119', '인천': '#0082C8', '광주': '#F58231',
    '대전': '#911EB4', '울산': '#46F0F0', '세종': '#F032E6', '경기': '#D2F53C', '강원': '#FABEBE',
    '충북': '#008080', '충남': '#E6BEFF', '전북': '#AA6E28', '전남': '#800000', '경북': '#000000',
    '경남': '#A9A9A9', '제주': '#FFD700'
}

final_heart_df.info()
final_heart_df.describe()

heart_occur_melted = heart_occur.melt(id_vars=['연도', '시도'], 
                                      value_vars=['전체 발생률'],
                                      var_name='변수', value_name='값')
heart_live_melted = heart_live.melt(id_vars=['연도', '시도'], 
                                      value_vars=['전체 생존율'],
                                      var_name='변수', value_name='값')
heart_heal_melted = heart_heal.melt(id_vars=['연도', '시도'], 
                                      value_vars=['전체 뇌기능 회복률'],
                                      var_name='변수', value_name='값')

# 급성심정지 생존율과 뇌기능 회복률의 상관관계 확인
correlation1 = final_heart_df[['전체 생존율', '전체 뇌기능 회복률']].corr().iloc[0, 1]
print(f"급성심장정지 생존율과 뇌기능 회복률의 상관계수: {correlation1:.3f}")

plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='전체 뇌기능 회복률', y='전체 생존율')
plt.title(f'전체 생존율 vs 뇌기능 회복률 (상관계수: {correlation1:.3f})', fontsize=16)
plt.xlabel('전체 뇌기능 회복률 (%)', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.show()

# 급성심정지 생존율과 발생률의 상관관계 확인
correlation2 = final_heart_df[['전체 생존율', '전체 발생률']].corr().iloc[0, 1]
print(f"급성심장정지 생존율과 발생률의 상관계수: {correlation2:.3f}")


plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='전체 발생률', y='전체 생존율')
plt.title(f'전체 생존율 vs 전체 발생률 (상관계수: {correlation2:.3f})', fontsize=16)
plt.xlabel('전체 발생률 (%)', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.show()

# 병원 개수와 생존율의 상관관계 확인
correlation3 = final_heart_df[['병원 합계', '전체 생존율']].corr().iloc[0, 1]
print(f"병원합계와 생존율의 상관계수: {correlation3:.3f}")

plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='병원 합계', y='전체 생존율')
plt.title(f'병원 합계 vs 전체 발생률 (상관계수: {correlation3:.3f})', fontsize=16)
plt.xlabel('병원 합계', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.show()

# 병원 개수와 뇌기능 회복률의 상관관계 확인
correlation4 = final_heart_df[['병원 합계', '전체 뇌기능 회복률']].corr().iloc[0, 1]
print(f"병원합계와 뇌기능 회복률의 상관계수: {correlation4:.3f}")

plt.figure(figsize=(6, 4))

sns.scatterplot(data=final_heart_df, x='병원 합계', y='전체 뇌기능 회복률')
plt.title(f'병원 합계 vs 전체 뇌기능 회복률 (상관계수: {correlation4:.3f})', fontsize=16)
plt.xlabel('병원 합계', fontsize=12)
plt.ylabel('전체 뇌기능 회복률', fontsize=12)
plt.show()

plt.figure(figsize=(15, 7))

sns.lineplot(data=heart_occur_melted, x='연도', y='값', hue='시도', marker='o', palette= palette)

plt.title('연도 및 시도별 급성심장정지 전체 발생률 추세 (2016-2019)', fontsize=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('전체 발생률 (%)', fontsize=12)
plt.xticks([2016, 2017, 2018, 2019])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 7))

sns.lineplot(data=heart_live_melted, x='연도', y='값', hue='시도', marker='o', palette= palette)

plt.title('연도 및 시도별 급성심장정지 전체 생존율 추세 (2016-2019)', fontsize=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('전체 생존율 (%)', fontsize=12)
plt.xticks([2016, 2017, 2018, 2019])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 7))

sns.lineplot(data=heart_heal_melted, x='연도', y='값', hue='시도', marker='o', palette= palette)

plt.title('연도 및 시도별 급성심장정지 전체 뇌기능 회복률 추세 (2016-2019)', fontsize=20)
plt.xlabel('연도', fontsize=12)
plt.ylabel('전체 뇌기능 회복률 (%)', fontsize=12)
plt.xticks([2016, 2017, 2018, 2019])
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

mean_df = final_heart_df.groupby('시도')['병원 합계'].mean().reset_index()

colors = [palette[sido] for sido in mean_df['시도']]

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