import requests
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from python_pt11_part1 import heart_occur_eng, heart_live_eng, heart_heal_eng, hospital_df_eng

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


# 병원 데이터 필요한 컬럼만 남기기 (연도, 시도, 종합병원, 일반병원)
hospital_df = hospital_df_eng[['연도', '시도', '병의원_종합병원', '병의원_일반병원']]

# 컬럼이름 수정
hospital_df = hospital_df.rename(columns={
    '병의원_종합병원': '종합병원',
    '병의원_일반병원': '일반병원'
})

# 시도 컬럼의 데이터 내용 수정 (ex. 서울 Seoul -> 서울)
hospital_df['시도'] = hospital_df['시도'].str[:2]

# 급성심장정지 데이터와 데이터 추출 연도 일치를 위해 2016-2019년도 데이터 추출
hospital_df = hospital_df[hospital_df['연도'].between(2016,2019)].reset_index(drop=True)

# 전체 데이터 합치기
final_heart_df = heart_live.merge(heart_heal, on=['연도', '시도'], how='left').\
    merge(heart_occur, on=['연도', '시도'], how='left').\
    merge(hospital_df, on=['연도', '시도'], how='left')
    
# 전체 병원 개수 컬럼 생성
final_heart_df['병원 합계'] = final_heart_df['종합병원'] + final_heart_df['일반병원']