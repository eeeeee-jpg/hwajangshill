"""Streamlit 진입점: 로고, 필터, 지도, 목록, 출처 표시.

정제 CSV(data/toilets_clean.csv)만 읽는다. API는 호출하지 않는다.
"""
import base64
import os

import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

import mission
from map_view import toilet_map

load_dotenv()

CSV_PATH = "data/toilets_clean.csv"
MAP_LIMIT = 200
ALL_DISTRICTS = "전체 구"
# 원본 '데이터기준일자' 컬럼의 최신값. 포털 표기와 다르면 고친다.
DATA_DATE = "2020-06-04"

st.set_page_config(page_title="공중화장실 찾기", page_icon=":material/wc:", layout="wide")

# 색은 DESIGN.md 토큰. 헤더는 로고와 필터만 두고 지도·목록이 화면 중심이 되게 한다
st.html("""
<style>
@import url("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&display=swap");
.block-container { padding-top: 3.25rem; padding-bottom: 1rem; }
::selection { background: #E4D0F2; color: #25232A; }
/* 좁은 화면에서도 로고와 구 선택을 한 줄에 */
.st-key-topbar [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; }
.st-key-topbar [data-testid="stColumn"]:first-child { flex: 1 1 auto; min-width: 0; }
.st-key-topbar [data-testid="stColumn"]:last-child { flex: 0 0 9.5rem; width: 9.5rem; min-width: 0; }
.st-key-topbar { border-bottom: 2px solid #25232A; padding: 0 0 10px; }
.logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo img { width: 36px; height: 36px; flex: none; }
.logo-word { margin: 0; font-size: 22px; font-weight: 900; letter-spacing: -.03em; line-height: 1; color: #25232A; }
.logo-word .hot { color: #7B2CBF; }
.logo-word .bang { display: inline-block; color: #7B2CBF; transform-origin: 50% 90%;
  animation: logo-shake 1.4s ease-in-out infinite; }
@keyframes logo-shake { 0%, 60%, 100% { transform: rotate(0); } 70% { transform: rotate(14deg); } 80% { transform: rotate(-10deg); } 90% { transform: rotate(6deg); } }
@media (prefers-reduced-motion: reduce) { .logo-word .bang { animation: none; } }
@media (max-width: 640px) { .logo-word { font-size: 19px; } .logo img { width: 30px; height: 30px; } }
</style>
""")

# 로고 마크: 코스 보라 위 크림색 변기 아이콘 (st.html은 인라인 SVG를 지우므로 <img>로)
LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
    '<rect width="40" height="40" rx="8" fill="#7B2CBF"/>'
    '<g transform="translate(8 8)" fill="none" stroke="#F7F3EA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M7 12h13a1 1 0 0 1 1 1 5 5 0 0 1-5 5h-.6a.5.5 0 0 0-.42.77l1.54 2.47a.5.5 0 0 1-.42.76H5.4a.5.5 0 0 1-.42-.76L7 18"/>'
    '<path d="M8 18a5 5 0 0 1-5-5V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8"/></g></svg>'
)
LOGO_SRC = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode()).decode()


def distance_km(lat, lng, lats, lngs):
    """(lat, lng)에서 각 좌표까지의 직선 거리(km, 하버사인)."""
    lat1, lng1, lat2, lng2 = map(np.radians, (lat, lng, lats, lngs))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lng2 - lng1) / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(a))


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


try:
    df = load_data()
except FileNotFoundError:
    st.error(f"{CSV_PATH} 파일이 없습니다. 먼저 `python prepare_data.py`를 실행하세요.")
    st.stop()

logo_col, gu_col = st.container(key="topbar").columns([4, 1], vertical_alignment="center")
logo_col.html(
    f'<div class="logo"><img src="{LOGO_SRC}" alt="">'
    '<h1 class="logo-word"><span class="hot">급똥</span>화장실필요<span class="bang">!</span></h1></div>'
)
선택구 = gu_col.selectbox("구", [ALL_DISTRICTS, *sorted(df["구"].dropna().unique())], label_visibility="collapsed")
# 조건은 지도 바로 위 칩으로: 개방구분 두 개는 고른 것끼리 합치고, 장애인용은 추가로 거른다
CONDITIONS = {"24시간": "24시간", "시간제한": "시간제한", "장애인용": ":material/accessible: 장애인용"}
조건 = st.pills("조건", list(CONDITIONS), selection_mode="multi", format_func=CONDITIONS.get, label_visibility="collapsed")

# 위치는 지도 컴포넌트가 브라우저에서 받아 상태로 남긴다 (첫 실행엔 아직 없음)
pos = (st.session_state.get("toilet_map") or {}).get("pos")
me = (pos["lat"], pos["lng"]) if pos else None

# 필터 결과는 df_f 하나로 만들고 지도·목록이 모두 이것만 쓴다
df_f = df.copy()
if 선택구 != ALL_DISTRICTS:
    df_f = df_f[df_f["구"] == 선택구]
구분 = [k for k in ("24시간", "시간제한") if k in 조건]
if 구분:
    df_f = df_f[df_f["개방구분"].isin(구분)]
if "장애인용" in 조건:
    df_f = df_f[df_f["장애인용"]]
if me:
    df_f = df_f.assign(거리=distance_km(*me, df_f["위도"], df_f["경도"])).sort_values("거리")

df_map = df_f.head(MAP_LIMIT)
selected = None

if df_f.empty:
    st.info("조건에 맞는 화장실이 없습니다. 필터를 바꿔 보세요.")
js_key = os.getenv("KAKAO_JS_KEY") or st.secrets.get("KAKAO_JS_KEY")
if js_key:
    picked = toilet_map(js_key, df_map, me=me).get("picked")
    if picked:
        hit = df_map[
            (df_map["이름"] == picked["name"])
            & np.isclose(df_map["위도"], picked["lat"])
            & np.isclose(df_map["경도"], picked["lng"])
        ]
        selected = hit.iloc[0] if len(hit) else None
else:
    st.warning("KAKAO_JS_KEY가 없어 지도를 표시할 수 없습니다.")

if len(df_f) > MAP_LIMIT:
    기준 = "가까운" if me else "앞의"
    st.caption(f"조건에 맞는 {len(df_f):,}곳 중 {기준} {MAP_LIMIT}곳만 지도에 올립니다.")
st.caption(f"출처: 공공데이터포털 전국공중화장실표준데이터 · 데이터 기준일 {DATA_DATE}")

# 미션 체크리스트는 화면에서 뺐다: 화장실을 고르기만 하면 완료
mission.render(None, True, selected)
