import requests
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

load_dotenv()

# url과 파라미터 설정 + 결과 확인
url = 'http://apis.data.go.kr/1352000/ODMS_STAT_09/callStat09Api'
key = os.getenv("SERVICE_KEY")
params ={'serviceKey' : f'{key}', 'apiType' : 'JSON'}

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
        
        # 급성심장정지 발생률
heart_occur_eng = api_df('08')

# 급성심장정지 생존율
heart_live_eng = api_df('09')

# 급성심장정지 뇌기능 회복률
heart_heal_eng = api_df('10')

# 전국 병원 데이터 csv 파일 불러오기
hospital_df_eng = pd.read_csv("보건복지부_병원 및 의원 수_의료기관 종류별_시도별_20221231.csv", encoding='cp949')