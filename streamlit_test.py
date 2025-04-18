import streamlit as st
import pandas as pd

st.set_page_config(page_title="급성심장정지", layout="wide")
st.title("💓 급성심장정지")

@st.cache_data
def load_data():
    final_df = pd.read_csv("final_heart_df.csv")
    occur = pd.read_csv("heart_occur.csv")
    live = pd.read_csv("heart_live.csv")
    heal = pd.read_csv("heart_heal.csv")
    return final_df, occur, live, heal 

final_df, occur_df, live_df, heal_df = load_data() 

year_options = ['전체'] + sorted(final_df['연도'].dropna().unique().astype(str).tolist())
city_options = ['전체'] + sorted(final_df['시도'].dropna().unique().tolist())

st.sidebar.header("🔎 필터링 옵션")
selected_year = st.sidebar.selectbox("연도 선택", year_options)
selected_city = st.sidebar.selectbox("시도 선택", city_options)
filter_button = st.sidebar.button("검색")

def filter_df(df, year, city):
    if year != '전체':
        df = df[df['연도'].astype(str) == year]
    if city != '전체':
        df = df[df['시도'] == city]
    return df

if 'filtered' not in st.session_state or not filter_button:
    st.session_state.filtered = {
        "final": final_df,
        "occur": occur_df,
        "live": live_df,
        "heal": heal_df
    }  # hospital 제거

if filter_button:
    st.session_state.filtered["final"] = filter_df(final_df, selected_year, selected_city)
    st.session_state.filtered["occur"] = filter_df(occur_df, selected_year, selected_city)
    st.session_state.filtered["live"] = filter_df(live_df, selected_year, selected_city)
    st.session_state.filtered["heal"] = filter_df(heal_df, selected_year, selected_city)

def display_dataframe(df):
    """연도 컬럼만 정수 포맷팅하는 함수"""
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "연도": st.column_config.NumberColumn(format="%d") 
        }
    )

tab1, tab2, tab3, tab4 = st.tabs(["전체", "발생률", "생존률", "회복률"])  

with tab1:
    st.subheader("전체 지표")
    
    st.markdown("""
        <style>
        div[data-baseweb="select"] {
            width: 200px !important;
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
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-baseweb="select"] {
            margin-left: auto !important;
            margin-right: 0 !important;
            width: 250px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    keyword = st.selectbox(
        "",
        options=["(선택 안함)", "전체", "질병", "질병외"],
        index=0,
        label_visibility="collapsed"
    )
    
    # 컬럼 필터링 함수 (질병/질병외 완전 분리)
    def filter_columns_containing_keyword(df, keyword):
        base_cols = ['연도', '시도']
        if keyword == "(선택 안함)":
            return df
        elif keyword == "전체":
            return df[base_cols + [col for col in df.columns if '전체' in col]]   
        elif keyword == "질병":
            return df[base_cols + [col for col in df.columns if '질병' in col and '질병외' not in col]]
        else:  # 질병외
            return df[base_cols + [col for col in df.columns if '질병외' in col]]
    
    # 필터 적용
    filtered_final = filter_columns_containing_keyword(
        st.session_state.filtered["final"], 
        keyword
    )
    
    # 출력
    display_dataframe(filtered_final)


with tab2:
    st.subheader("발생률")
    display_dataframe(st.session_state.filtered["occur"])

with tab3:
    st.subheader("생존률")
    display_dataframe(st.session_state.filtered["live"])

with tab4:
    st.subheader("회복률")
    display_dataframe(st.session_state.filtered["heal"])