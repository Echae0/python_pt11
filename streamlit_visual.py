# 💓 급성심장정지

import streamlit as st
import pandas as pd
from python_pt11_part3 import occur, live, heal, hospital

st.set_page_config(page_title="급성심장정지", layout="wide")
st.title("💓 급성심장정지")

palette = {
    '서울': '#E6194B', '부산': '#3CB44B', '대구': '#FFE119', '인천': '#0082C8', '광주': '#F58231',
    '대전': '#911EB4', '울산': '#46F0F0', '세종': '#F032E6', '경기': '#D2F53C', '강원': '#FABEBE',
    '충북': '#008080', '충남': '#E6BEFF', '전북': '#AA6E28', '전남': '#800000', '경북': '#000000',
    '경남': '#A9A9A9', '제주': '#FFD700'
}

@st.cache_data
def load_data():
    final_df = pd.read_csv("final_heart_df.csv")
    occur = pd.read_csv("heart_occur.csv")
    live = pd.read_csv("heart_live.csv")
    heal = pd.read_csv("heart_heal.csv")
    hospital = pd.read_csv("hospital_df.csv")
    return final_df, occur, live, heal , hospital

final_df, occur_df, live_df, heal_df, hospital_df = load_data() 

year_options = ['전체'] + sorted(final_df['연도'].dropna().unique().astype(str).tolist())
city_options = ['전체'] + sorted(final_df['시도'].dropna().unique().tolist())

st.sidebar.header("🔎 필터링 옵션")
selected_year = st.sidebar.selectbox("연도 선택", year_options)
selected_city = st.sidebar.selectbox("시도 선택", city_options)

st.sidebar.markdown("적용할 탭 선택")

checkbox_items = ["전체", "발생률", "생존률", "회복률", "병원 수"]

for item in checkbox_items:
    if item not in st.session_state:
        st.session_state[item] = False

if "모두 선택" not in st.session_state:
    st.session_state["모두 선택"] = False

def select_all_tabs():
    for item in checkbox_items:
        st.session_state[item] = st.session_state["모두 선택"]

def check_if_all_selected():
    if any(not st.session_state[item] for item in checkbox_items):        
        st.session_state["모두 선택"] = False
    else:
        st.session_state["모두 선택"] = True

tab_checkboxes = {}
for item in checkbox_items:
    tab_checkboxes[item] = st.sidebar.checkbox(item, key=item, on_change=check_if_all_selected)

def select_all_tabs():
    for item in checkbox_items:
        st.session_state[item] = st.session_state["모두 선택"]

st.sidebar.checkbox("모두 선택", key="모두 선택", on_change=select_all_tabs)
filter_button = st.sidebar.button("검색")

def filter_df(df, year, city):
    if year != '전체':
        df = df[df['연도'].astype(str) == year]
    if city != '전체':
        df = df[df['시도'] == city]
    return df

def apply_filtering():
    filtered_data = {}
    if tab_checkboxes["전체"]:
        filtered_data["final"] = filter_df(final_df, selected_year, selected_city)
    if tab_checkboxes["발생률"]:
        filtered_data["occur"] = filter_df(occur_df, selected_year, selected_city)
    if tab_checkboxes["생존률"]:
        filtered_data["live"] = filter_df(live_df, selected_year, selected_city)
    if tab_checkboxes["회복률"]:
        filtered_data["heal"] = filter_df(heal_df, selected_year, selected_city)
    if tab_checkboxes["병원 수"]:
        filtered_data["hospital"] = filter_df(hospital_df, selected_year, selected_city)
    return filtered_data

if 'filtered' not in st.session_state or not filter_button:
    st.session_state.filtered = {
        "final": final_df,
        "occur": occur_df,
        "live": live_df,
        "heal": heal_df,
        "hospital": hospital_df
    }

if filter_button:
    if any(st.session_state[item] for item in checkbox_items):
        st.session_state.filtered.update(apply_filtering())

def display_dataframe(df):
    """연도 컬럼만 정수 포맷팅하는 함수"""
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "연도": st.column_config.TextColumn() 
        }
    )

def selectionbox_item(key):
    st.markdown("""
        <style>
        div[data-baseweb="select"] {
            width: 150px !important;
            height: 50px !important;
        }
        div[data-baseweb="select"] > div {
            padding-top: 2px !important;
            padding-bottom: 2px !important;
            min-height: 40px !important; 
        }
        div[data-baseweb="select"] {
            font-size: 15px !important; 
        }
        </style>
    """, unsafe_allow_html=True)

    keyword = st.selectbox(
        "",  
        options=["(선택 안함)", "전체", "질병", "질병외"],
        index=0,
        label_visibility="collapsed",
        key=key
    )
    return keyword

def hospital_selectionbox(key):
    st.markdown("""
        <style>
        div[data-baseweb="select"] {
            width: 150px !important;
            height: 50px !important;
        }
        div[data-baseweb="select"] > div {
            padding-top: 2px !important;
            padding-bottom: 2px !important;
            min-height: 40px !important; 
        }
        div[data-baseweb="select"] {
            font-size: 15px !important; 
        }
        </style>
    """, unsafe_allow_html=True)

    keyword = st.selectbox(
        "", 
        options=["(선택 안함)", "종합병원", "일반병원"],
        index=0,
        label_visibility="collapsed",
        key=key
    )
    return keyword

def filter_and_display(df_key, tab_key):
    df = st.session_state.filtered[df_key]
    base_cols = ['연도', '시도']
    keyword = selectionbox_item(tab_key)
    
    if keyword == "(선택 안함)":
        filtered = df
    elif keyword == "전체":
        filtered = df[base_cols + [col for col in df.columns if '전체' in col]]
    elif keyword == "질병":
        filtered = df[base_cols + [col for col in df.columns if '질병' in col and '질병외' not in col]]
    else:
        filtered = df[base_cols + [col for col in df.columns if '질병외' in col]]
    
    display_dataframe(filtered)

def hospital_filter_and_display(df_key, tab_key):
    df = st.session_state.filtered[df_key]
    base_cols = ['연도', '시도']
    keyword = hospital_selectionbox(tab_key)
    
    if keyword == "(선택 안함)":
        filtered = df
    elif keyword == "종합병원":
        filtered = df[base_cols + [col for col in df.columns if '종합병원' in col]]
    else:
        filtered = df[base_cols + [col for col in df.columns if '일반병원' in col]]
    
    display_dataframe(filtered)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["전체", "발생률", "생존률", "회복률", "병원 수"])  

with tab1:
    st.subheader("전체 지표")
    filter_and_display("final", "tab1")


with tab2:
    st.subheader("발생률")
    filter_and_display("occur", "tab2")

    st.divider()

    st.subheader("전체 발생률 추세")
    occur(occur,palette)

with tab3:
    st.subheader("생존률")
    filter_and_display("live", "tab3")

    st.divider()
    
    st.subheader("전체 생존률 추세")
    live(live,palette)

with tab4:
    st.subheader("회복률")
    filter_and_display("heal", "tab4")

    st.divider()
    
    st.subheader("전체 회복률 추세")
    heal(heal,palette)

with tab5:
    st.subheader("병원 수")
    hospital_filter_and_display("hospital", "tab5")

    st.divider()
    
    st.subheader("지역별 평균 병원 수")
    hospital(hospital,palette)