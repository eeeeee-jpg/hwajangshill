"""카카오 지도 + '지금 지도에 보이는 화장실' 목록 컴포넌트. (JavaScript 키만 사용)

st.components.v2 로 페이지 안에서 실행되므로 브라우저 위치를 받고,
지도를 움직일 때마다 화면 안의 화장실만 목록에 다시 그린다.
"""
import pandas as pd
import streamlit as st

MAX_MARKERS = 200
SEOUL_CITY_HALL = (37.5665, 126.9780)

HTML = """<div class="tl-wrap">
  <div class="tl-map" role="region" aria-label="화장실 지도"></div>
  <section class="tl-side" aria-label="지금 지도에 보이는 화장실">
    <header class="tl-head">
      <p class="tl-count" role="status"></p>
      <button type="button" class="tl-locate">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.5"/>
          <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>
        <span>내 위치</span>
      </button>
    </header>
    <p class="tl-msg" role="status"></p>
    <ul class="tl-list"></ul>
  </section>
</div>"""

CSS = """
/* 지도·목록이 화면 대부분을 차지하게: 화면 높이에서 헤더·출처만큼 뺀다 (최소 520) */
.tl-wrap { display: grid; grid-template-columns: 3fr 2fr; gap: 16px; height: max(520px, calc(100dvh - 210px));
  font-family: Pretendard, system-ui, sans-serif; color: #222222; }
.tl-map { height: 100%; border-radius: 16px; overflow: hidden; background: #F0F2F9; }
.tl-side { display: flex; flex-direction: column; min-height: 0; background: #FFFFFF;
  border: 1px solid #F0F2F9; border-radius: 16px; padding: 16px; }
.tl-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.tl-count { margin: 0; font-size: 16px; font-weight: 700; }
.tl-locate { display: inline-flex; align-items: center; gap: 6px; min-height: 40px; padding: 0 14px;
  border: 1px solid #FF52A3; border-radius: 999px; background: #FFF2F9; color: #222222;
  font: 600 14px Pretendard, system-ui, sans-serif; cursor: pointer; }
.tl-locate:hover { background: #FFD2E7; }
.tl-msg { margin: 8px 0 0; font-size: 12px; color: #717686; }
.tl-msg:empty { display: none; }
.tl-list { list-style: none; margin: 12px 0 0; padding: 0; overflow-y: auto; flex: 1; }
.tl-item { display: block; width: 100%; text-align: left; padding: 12px; border: 1px solid transparent;
  border-bottom-color: #F0F2F9; border-radius: 12px; background: none; cursor: pointer;
  font-family: inherit; color: inherit; transition: background-color .15s ease; }
.tl-item:hover { background: #F8F9FD; }
.tl-item.tl-on { background: #FFF2F9; border-color: #FF52A3; }
.tl-wrap button:focus-visible { outline: 3px solid #222222; outline-offset: 2px; }
.tl-name { display: flex; justify-content: space-between; gap: 8px; font-size: 16px; font-weight: 700; }
.tl-dist { flex: none; font-size: 14px; font-weight: 600; color: #FF007F; }
.tl-meta { margin-top: 4px; font-size: 12px; color: #717686; }
.tl-kind { font-weight: 700; color: #505462; }
.tl-me { width: 14px; height: 14px; border-radius: 50%; background: #FF52A3; border: 3px solid #FFFFFF;
  box-shadow: 0 0 0 6px rgba(255, 82, 163, .25); }
@media (max-width: 640px) {
  .tl-wrap { grid-template-columns: 1fr; height: auto; }
  .tl-map { height: 360px; }
  .tl-list { max-height: 420px; }
}
"""

JS = """
let sdk;
function loadSdk(key) {
  sdk = sdk || new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = "https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=" + encodeURIComponent(key);
    s.onload = () => kakao.maps.load(resolve);
    s.onerror = reject;
    document.head.appendChild(s);
  });
  return sdk;
}

function locate(st, setStateValue) {
  if (!navigator.geolocation) { st.msg.textContent = "이 브라우저는 위치 기능을 지원하지 않아요."; return; }
  st.msg.textContent = "내 위치를 찾는 중…";
  navigator.geolocation.getCurrentPosition(
    (p) => { st.msg.textContent = ""; setStateValue("pos", { lat: p.coords.latitude, lng: p.coords.longitude }); },
    () => { st.msg.textContent = "위치를 받지 못했어요. 브라우저에서 위치 권한을 허용하면 가까운 순으로 보여 줘요."; },
    { enableHighAccuracy: true, timeout: 10000 }
  );
}

function km(d) { return d < 1 ? Math.round(d * 1000) + "m" : d.toFixed(1) + "km"; }

function renderList(st) {
  const bounds = st.map.getBounds();
  const visible = st.items.filter((it) => bounds.contain(it.pos));
  st.count.textContent = "지금 지도에 보이는 화장실 " + visible.length + "곳";
  st.list.replaceChildren(...visible.map((it) => {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.type = "button";
    b.className = "tl-item" + (it === st.selected ? " tl-on" : "");
    const name = document.createElement("div");
    name.className = "tl-name";
    name.append(it.t.name);
    if (it.t.dist != null) {
      const d = document.createElement("span"); d.className = "tl-dist"; d.textContent = km(it.t.dist); name.append(d);
    }
    const meta = document.createElement("div");
    meta.className = "tl-meta";
    const kind = document.createElement("span"); kind.className = "tl-kind"; kind.textContent = it.t.kind;
    meta.append(kind, " | " + it.t.addr);
    b.append(name, meta);
    b.onclick = () => st.pick(it, true);
    li.append(b);
    return li;
  }));
  if (!visible.length) st.list.innerHTML = '<li class="tl-meta">이 화면에는 화장실이 없어요. 지도를 축소해 보세요.</li>';
}

export default function ({ parentElement, data, setStateValue }) {
  const mapEl = parentElement.querySelector(".tl-map");
  const st = mapEl.__tl || (mapEl.__tl = {
    count: parentElement.querySelector(".tl-count"),
    list: parentElement.querySelector(".tl-list"),
    msg: parentElement.querySelector(".tl-msg"),
  });
  parentElement.querySelector(".tl-locate").onclick = () => locate(st, setStateValue);
  // 첫 화면에서 바로 위치를 묻는다 (한 번만)
  if (!data.me && !st.asked) { st.asked = true; locate(st, setStateValue); }

  const sig = JSON.stringify(data);
  if (st.sig === sig) return;
  const prevMe = st.me;
  st.sig = sig;
  st.me = JSON.stringify(data.me);

  loadSdk(data.key).then(() => {
    const LL = (p) => new kakao.maps.LatLng(p[0], p[1]);  // LatLng(위도, 경도) 순서
    if (!st.map) {
      st.map = new kakao.maps.Map(mapEl, { center: LL(data.me || data.center), level: 5 });
      st.map.addControl(new kakao.maps.ZoomControl(), kakao.maps.ControlPosition.BOTTOMRIGHT);
      st.info = new kakao.maps.InfoWindow({ removable: true });
      kakao.maps.event.addListener(st.map, "idle", () => renderList(st));
      // 화면 폭이 바뀌면(모바일 회전 등) 지도 크기를 다시 계산한다
      new ResizeObserver(() => { const c = st.map.getCenter(); st.map.relayout(); st.map.setCenter(c); }).observe(mapEl);
      st.pick = (it, pan) => {
        st.selected = it;
        const box = document.createElement("div");
        box.style.cssText = "padding:8px;font-size:12px;white-space:nowrap;";
        const b = document.createElement("b"); b.textContent = it.t.name;
        box.append(b, document.createElement("br"), "개방시간: " + it.t.hours);
        st.info.setContent(box);
        st.info.open(st.map, it.marker);
        if (pan) st.map.panTo(it.pos);
        renderList(st);
        setStateValue("picked", { name: it.t.name, lat: it.t.lat, lng: it.t.lng });
      };
    }
    (st.items || []).forEach((it) => it.marker.setMap(null));
    st.info.close();
    st.selected = null;
    st.items = data.toilets.map((t) => {
      const it = { t, pos: LL([t.lat, t.lng]) };
      it.marker = new kakao.maps.Marker({ map: st.map, position: it.pos, title: t.name });
      kakao.maps.event.addListener(it.marker, "click", () => st.pick(it, false));
      return it;
    });

    if (st.meDot) st.meDot.setMap(null);
    if (data.me) {
      st.meDot = new kakao.maps.CustomOverlay({ map: st.map, position: LL(data.me), content: '<div class="tl-me" title="내 위치"></div>' });
    }
    if (st.me !== prevMe && data.me) {
      // 내 위치를 크게 확대하되, 가까운 3곳은 화면에 들어오게 (한 곳이 닫혀 있을 수도 있으니)
      st.map.setCenter(LL(data.me));
      st.map.setLevel(2);
      const nearest = st.items[Math.min(2, st.items.length - 1)];
      while (nearest && !st.map.getBounds().contain(nearest.pos) && st.map.getLevel() < 8) {
        st.map.setLevel(st.map.getLevel() + 1);
      }
    }
    renderList(st);
  }, () => { st.msg.textContent = "지도를 불러오지 못했어요. 잠시 후 새로고침해 주세요."; });
}
"""

_component = st.components.v2.component("toilet_map", html=HTML, css=CSS, js=JS, isolate_styles=False)


def toilet_map(js_key, df, me=None):
    """df(이름·주소·위도·경도·개방시간·개방구분, 선택: 거리) 앞 200곳을 지도와 목록으로 그린다.

    me: (위도, 경도) 현재 위치. 주면 그 주변을 크게 확대해 보여 준다.
    돌려주는 값: pos(브라우저가 준 현재 위치), picked(목록·마커에서 고른 화장실의 이름·위도·경도).
    """
    rows = df.head(MAX_MARKERS)
    toilets = [
        {
            "lat": float(r["위도"]),
            "lng": float(r["경도"]),
            "name": str(r["이름"]),
            "addr": str(r["주소"]),
            "kind": str(r["개방구분"]),
            "hours": str(r["개방시간"]) if pd.notna(r["개방시간"]) else "정보없음",
            "dist": float(r["거리"]) if "거리" in r else None,
        }
        for _, r in rows.iterrows()
    ]
    center = (rows["위도"].mean(), rows["경도"].mean()) if toilets else SEOUL_CITY_HALL
    return _component(
        key="toilet_map",
        data={"key": js_key, "toilets": toilets, "me": list(me) if me else None, "center": list(center)},
        on_pos_change=lambda: None,
        on_picked_change=lambda: None,
    )

