"""전국공중화장실표준데이터 중 서울 원본 → data/toilets_clean.csv.

실행: python prepare_data.py
필요: data/raw/seoul_toilets.csv, .env의 KAKAO_REST_API_KEY
"""
import os
import re

import pandas as pd
import requests
from dotenv import load_dotenv

RAW = "data/raw/seoul_toilets.csv"
OUT = "data/toilets_clean.csv"
SIDO = "서울"
# 서울 대략 경계. 이 밖의 좌표는 잘못된 값으로 보고 다시 변환한다.
LAT_RANGE = (37.4, 37.72)
LNG_RANGE = (126.76, 127.19)

TIME = r"\d{1,2}[:;]\d{2}|\d{1,2}시(?!간)"  # 09:00, 06;00(오타), 09시
ALL_DAY = rf"00:00\s*[~-]\s*24:00"


def classify_hours(text):
    """개방시간 자유 텍스트 → 24시간 / 시간제한 / 정보없음."""
    if not isinstance(text, str) or not text.strip():
        return "정보없음"
    # 00:00~24:00 외의 시간 범위가 하나라도 있으면 시간제한
    if re.search(TIME, re.sub(ALL_DAY, "", text)):
        return "시간제한"
    # 연중무휴는 시간 정보가 없지만 팀 합의로 24시간으로 본다
    if re.search(rf"24시간|상시|연중무휴|{ALL_DAY}", text):
        return "24시간"
    return "정보없음"


def geocode(address, key):
    """카카오 로컬 API 주소 검색. 실패하면 (None, None)."""
    res = requests.get(
        "https://dapi.kakao.com/v2/local/search/address.json",
        headers={"Authorization": f"KakaoAK {key}"},
        params={"query": address},
        timeout=10,
    )
    res.raise_for_status()
    docs = res.json()["documents"]
    if not docs:
        return None, None
    return float(docs[0]["y"]), float(docs[0]["x"])


def main():
    load_dotenv()
    key = os.getenv("KAKAO_REST_API_KEY")
    if not key:
        raise SystemExit(".env에 KAKAO_REST_API_KEY가 없습니다.")

    raw = pd.read_csv(RAW, dtype=str)
    raw["주소"] = raw["소재지도로명주소"].fillna(raw["소재지지번주소"]).str.strip()
    raw = raw[raw["주소"].str.startswith(SIDO, na=False)].copy()

    df = pd.DataFrame({
        "이름": raw["화장실명"].str.strip(),
        "주소": raw["주소"],
        "구": raw["주소"].str.split().str[1],
        "위도": pd.to_numeric(raw["위도"], errors="coerce"),
        "경도": pd.to_numeric(raw["경도"], errors="coerce"),
        "개방시간": raw["개방시간"],
        "개방구분": raw["개방시간"].map(classify_hours),
        "장애인용": (
            pd.to_numeric(raw["남성용-장애인용대변기수"], errors="coerce").fillna(0)
            + pd.to_numeric(raw["여성용-장애인용대변기수"], errors="coerce").fillna(0)
        ) >= 1,
    })

    bad = ~(df["위도"].between(*LAT_RANGE) & df["경도"].between(*LNG_RANGE))
    print(f"서울 {len(df)}곳, 좌표 결측·오류 {bad.sum()}곳 변환 시작")
    for i in df.index[bad]:
        df.loc[i, ["위도", "경도"]] = geocode(df.at[i, "주소"], key)

    failed = ~(df["위도"].between(*LAT_RANGE) & df["경도"].between(*LNG_RANGE))
    print(f"좌표 변환 실패 {failed.sum()}곳 제외")
    df = df[~failed]

    dup = df.duplicated(["이름", "위도", "경도"])
    print(f"중복 {dup.sum()}곳 제외")
    df = df[~dup]

    os.makedirs("data", exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"{OUT} 저장: {len(df)}곳")
    print(df["개방구분"].value_counts().to_string())


if __name__ == "__main__":
    main()
