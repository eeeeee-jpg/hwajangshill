"""Streamlit 진입점: 필터, metric, 지도, 표, 출처 표시.

정제 CSV(data/toilets_clean.csv)만 읽는다. API는 호출하지 않는다.
"""
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from map_view import kakao_map_html

load_dotenv()

CSV_PATH = "data/toilets_clean.csv"
MAP_LIMIT = 200
ALL_DISTRICTS = "전체 구"
# 원본 '데이터기준일자' 컬럼의 최신값. 포털 표기와 다르면 고친다.
DATA_DATE = "2020-06-04"

st.set_page_config(page_title="공중화장실 찾기", page_icon="🚻", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


try:
    df = load_data()
except FileNotFoundError:
    st.error(f"{CSV_PATH} 파일이 없습니다. 먼저 `python prepare_data.py`를 실행하세요.")
    st.stop()

st.title("🚻 공중화장실 찾기")
st.markdown("**서울에서 지금 갈 수 있는 화장실은 어디일까?** 조건을 고르면 바로 걸러 보여줍니다.")

# 필터 (지도 위)
with st.container(border=True):
    filter_col1, filter_col2, filter_col3, _ = st.columns([2, 2, 2, 3], vertical_alignment="bottom")
    선택구 = filter_col1.selectbox(
        "구",
        [ALL_DISTRICTS, *sorted(df["구"].dropna().unique())],
    )
    구분 = filter_col2.selectbox(
        "개방 구분",
        ["전체", "24시간", "시간제한"],
    )
    장애인용만 = filter_col3.checkbox("장애인용만 보기")

# 필터 결과는 df_f 하나로 만들고 metric·지도·표가 모두 이것만 쓴다
df_f = df.copy()
if 선택구 != ALL_DISTRICTS:
    df_f = df_f[df_f["구"] == 선택구]
if 구분 != "전체":
    df_f = df_f[df_f["개방구분"] == 구분]
if 장애인용만:
    df_f = df_f[df_f["장애인용"]]

if df_f.empty:
    st.info("조건에 맞는 화장실이 없습니다. 조건을 바꿔 보세요.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("조건에 맞는 화장실", f"{len(df_f):,}곳")
    col2.metric("24시간 개방", f"{(df_f['개방구분'] == '24시간').sum():,}곳")
    col3.metric("장애인용 비율", f"{df_f['장애인용'].mean():.0%}")

    df_map = df_f.head(MAP_LIMIT)
    with st.container(border=True):
        st.subheader("지도")
        js_key = os.getenv("KAKAO_JS_KEY") or st.secrets.get("KAKAO_JS_KEY")
        if js_key:
            components.html(kakao_map_html(js_key, df_map), height=520)
        else:
            st.warning("KAKAO_JS_KEY가 없어 지도를 표시할 수 없습니다.")
    if len(df_f) > MAP_LIMIT:
        st.caption(f"전체 {len(df_f):,}곳 중 {MAP_LIMIT}곳만 지도에 표시합니다.")

    st.subheader("목록")
    # bool 그대로 두면 체크박스로 보여서 선택 가능한 것처럼 느껴지므로 ✔ 문자로 바꿔 표시
    df_table = df_f[["이름", "주소", "구", "개방시간", "개방구분", "장애인용"]].assign(
        장애인용=df_f["장애인용"].map({True: "✔", False: ""})
    )
    st.dataframe(
        df_table,
        hide_index=True,
        width="stretch",
    )

st.caption(f"출처: 공공데이터포털 전국공중화장실표준데이터 · 데이터 기준일 {DATA_DATE}")
