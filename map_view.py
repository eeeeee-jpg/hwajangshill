"""카카오 지도 + '지금 지도에 보이는 화장실' 범례 표 컴포넌트. (JavaScript 키만 사용)

st.components.v2 로 페이지 안에서 실행되므로 브라우저 위치를 받고,
지도를 움직일 때마다 화면 안의 화장실만 표에 다시 그린다.
오리엔티어링 지도처럼 화장실은 번호 원(컨트롤), 고른 곳까지는 보라 코스 선으로 그린다.
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
    <div class="tl-msg" role="status"></div>
    <div class="tl-body"></div>
    <p class="tl-key"><span class="tl-sym tl-sym-24"></span>24시간 <span class="tl-sym tl-sym-lim"></span>시간제한
      <span class="tl-sym tl-sym-none"></span>정보없음 · 시간은 직선거리로 어림한 도보 시간</p>
  </section>
</div>"""

CSS = """
/* 오리엔티어링 지도: 크림 종이, 잉크 선, 보라는 코스(고른 곳)에만 */
.tl-wrap { --paper: #F7F3EA; --ink: #25232A; --sub: #625E69; --rule: #E4DED2; --course: #7B2CBF; --course-20: #F1E7F8;
  display: grid; grid-template-columns: minmax(0, 1fr) 380px; gap: 16px; height: max(520px, calc(100dvh - 200px));
  font-family: inherit; color: var(--ink); font-variant-numeric: tabular-nums; }
.tl-map { height: 100%; border: 2px solid var(--ink); border-radius: 8px; overflow: hidden; background: #E8EBE3; }
.tl-side { display: flex; flex-direction: column; min-height: 0; background: var(--paper);
  border: 2px solid var(--ink); border-radius: 8px; padding: 14px 16px 10px; }
.tl-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.tl-count { margin: 0; font-size: 15px; font-weight: 700; }
.tl-locate { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 14px;
  border: 1.5px solid var(--ink); border-radius: 6px; background: #FFFFFF; color: var(--ink);
  font-family: inherit; font-size: 14px; font-weight: 600; cursor: pointer; transition: background-color .15s ease-out; }
.tl-locate:hover { background: var(--course-20); }
.tl-wrap button:focus-visible, .tl-wrap a:focus-visible { outline: 3px solid var(--course); outline-offset: 2px; }

.tl-msg:empty { display: none; }
.tl-note { margin-top: 10px; padding: 12px; border: 1.5px dashed #8C5A2B; border-radius: 8px; background: #FFFFFF; font-size: 13px; line-height: 1.5; }
.tl-note b { display: block; font-size: 14px; }
.tl-note button { margin-top: 8px; }

.tl-body { flex: 1; min-height: 0; overflow-y: auto; margin-top: 10px; }
.tl-th, .tl-row { display: grid; grid-template-columns: 34px minmax(0, 1fr) 52px 56px; align-items: center; gap: 6px; }
.tl-th { position: sticky; top: 0; z-index: 1; background: var(--paper); padding: 4px 0; border-bottom: 2px solid var(--ink);
  font-size: 12px; font-weight: 600; color: var(--sub); }
.tl-th span:last-child, .tl-min { text-align: right; }
.tl-list { list-style: none; margin: 0; padding: 0; }
.tl-row { width: 100%; min-height: 52px; padding: 4px 0; border: 0; border-bottom: 1px solid var(--rule); background: none;
  text-align: left; font-family: inherit; color: inherit; cursor: pointer; transition: background-color .15s ease-out; }
.tl-row:hover { background: #FFFFFF; }
.tl-row.tl-on { background: var(--course-20); }
.tl-no { font: 700 22px/1 "Barlow Condensed", sans-serif; color: var(--course); padding-left: 4px; }
.tl-name { font-size: 15px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tl-on .tl-name { font-weight: 700; }
.tl-syms { display: flex; align-items: center; gap: 6px; color: var(--sub); }
.tl-min { font: 700 19px/1 "Barlow Condensed", sans-serif; }
.tl-min small { display: block; margin-top: 2px; font-family: inherit; font-size: 11px; font-weight: 400; line-height: 1; color: var(--sub); }
.tl-gu { font-size: 13px; color: var(--sub); text-align: right; }

/* 개방구분은 색이 아니라 모양: 꽉 찬 원 24시간, 반원 시간제한, 빈 원 정보없음 */
.tl-sym { display: inline-block; width: 11px; height: 11px; border-radius: 50%; border: 1.5px solid var(--ink); vertical-align: -1px; }
.tl-sym-24 { background: var(--ink); }
.tl-sym-lim { background: linear-gradient(90deg, var(--ink) 50%, transparent 50%); }
.tl-wc { width: 16px; height: 16px; flex: none; }
.tl-key { margin: 8px 0 0; font-size: 12px; color: var(--sub); display: flex; flex-wrap: wrap; align-items: center; gap: 4px; }
.tl-key .tl-sym { margin-left: 4px; }

.tl-empty { text-align: center; padding: 28px 8px 8px; }
.tl-empty .tl-ring { width: 52px; height: 52px; margin: 0 auto 12px; border: 3px dashed var(--course); border-radius: 50%; }
.tl-empty p { margin: 0; font-size: 15px; font-weight: 700; }
.tl-empty small { display: block; margin: 4px 0 14px; font-size: 13px; color: var(--sub); }
.tl-ghost { display: flex; align-items: center; justify-content: center; width: 100%; min-height: 44px; border: 1.5px solid var(--course);
  border-radius: 6px; background: #FFFFFF; color: var(--course); font-family: inherit; font-size: 14px; font-weight: 700; cursor: pointer; }
.tl-ghost:hover { background: var(--course-20); }

.tl-card { border-top: 2px solid var(--ink); background: #FFFFFF; }
.tl-card h3 { display: flex; align-items: center; gap: 10px; margin: 0; padding: 12px; font-size: 17px; font-weight: 800; letter-spacing: -.02em; }
.tl-card h3 .tl-cname { min-width: 0; overflow-wrap: anywhere; }
.tl-num { flex: none; width: 30px; height: 30px; border: 3px solid var(--course); border-radius: 50%;
  display: grid; place-items: center; font: 700 17px/1 "Barlow Condensed", sans-serif; color: var(--course); }
.tl-card h3 .tl-cmin { margin-left: auto; flex: none; font: 700 24px/1 "Barlow Condensed", sans-serif; color: var(--course); }
.tl-kv { display: grid; grid-template-columns: 64px minmax(0, 1fr) auto; align-items: center; gap: 8px; padding: 10px 12px;
  border-top: 1px solid var(--rule); font-size: 13px; }
.tl-kv > span:first-child { font-size: 12px; font-weight: 600; color: var(--sub); }
.tl-kv > span:last-child { display: flex; align-items: center; gap: 6px; color: var(--sub); }
.tl-go { display: flex; align-items: center; gap: 8px; min-height: 48px; padding: 0 14px; background: var(--course); color: #FFFFFF !important;
  font-size: 15px; font-weight: 700; text-decoration: none; transition: background-color .15s ease-out; }
.tl-go:hover { background: #64209E; }
.tl-card + .tl-ghost { margin-top: 10px; }
.tl-caveat { margin: 8px 0 0; font-size: 12px; color: var(--sub); }

/* 지도 위 오버레이: 번호 원(컨트롤)과 내 위치 삼각형 */
/* 평소엔 원만 흐리게, 번호는 흰 테두리를 둘러 지도 위에서도 읽히게 */
.tl-ctl { position: relative; width: 26px; height: 26px; border: 3px solid rgba(123, 44, 191, .45); border-radius: 50%;
  background: rgba(255, 255, 255, .6); cursor: pointer; transition: border-color .15s ease-out; }
.tl-ctl b { position: absolute; left: 27px; top: -11px; font: 700 18px/1 "Barlow Condensed", sans-serif; color: var(--course);
  -webkit-text-stroke: 3px #FFFFFF; paint-order: stroke fill; }
.tl-ctl:hover, .tl-ctl.tl-on { border-color: var(--course); }
.tl-ctl.tl-on { width: 30px; height: 30px; background: rgba(255, 255, 255, .85); }
/* 넓게 보면 원이 겹치므로 번호를 숨기고 원을 줄인다 (고른 곳은 그대로) */
.tl-far .tl-ctl:not(.tl-on) { width: 12px; height: 12px; border-width: 2px; }
.tl-far .tl-ctl:not(.tl-on) b { display: none; }
.tl-me { width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent;
  border-bottom: 18px solid var(--course, #7B2CBF); filter: drop-shadow(0 1px 1px rgba(0, 0, 0, .35)); }

@media (max-width: 640px) {
  .tl-wrap { grid-template-columns: 1fr; height: auto; gap: 0; }
  .tl-map { height: max(300px, 52dvh); border-radius: 8px 8px 0 0; }
  .tl-side { border-top: 0; border-radius: 0 0 8px 8px; }
  .tl-body { overflow: visible; }
}
@media (prefers-reduced-motion: reduce) { .tl-wrap * { transition: none !important; } }
"""

JS = """
const WC = '<svg class="tl-wc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
  + 'stroke-linejoin="round" role="img" aria-label="장애인용"><circle cx="16" cy="4" r="1"/><path d="m18 19 1-7-6 1"/>'
  + '<path d="m5 8 3-3 5.5 3-2.36 3.5"/><path d="M4.24 14.5a5 5 0 0 0 6.88 6"/><path d="M13.76 17.5a5 5 0 0 0-6.88-6"/></svg>';
const KIND = { "24시간": "24", "시간제한": "lim" };

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

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

function sym(kind) {
  const s = el("span", "tl-sym tl-sym-" + (KIND[kind] || "none"));
  s.title = kind;
  return s;
}

function syms(t) {
  const box = el("span", "tl-syms");
  box.append(sym(t.kind));
  if (t.wc) box.insertAdjacentHTML("beforeend", WC);
  return box;
}

const minutes = (km) => Math.max(1, Math.round(km * 1000 / 80));  // 걷는 속도 분당 80m
const meters = (km) => km < 1 ? Math.round(km * 1000) + "m" : km.toFixed(1) + "km";

function locate(st, setStateValue) {
  if (!navigator.geolocation) { showNote(st, "이 브라우저는 위치 기능을 지원하지 않아요.", null); return; }
  st.msg.replaceChildren(el("p", "tl-key", "내 위치를 찾는 중…"));
  navigator.geolocation.getCurrentPosition(
    (p) => { st.msg.replaceChildren(); setStateValue("pos", { lat: p.coords.latitude, lng: p.coords.longitude }); },
    () => showNote(st, "지금은 조건에 맞는 곳을 모두 보여 줘요. 브라우저에서 위치를 허용하면 가까운 순으로 바뀌어요.",
      () => locate(st, setStateValue)),
    { enableHighAccuracy: true, timeout: 10000 }
  );
}

function showNote(st, text, retry) {
  const note = el("div", "tl-note");
  note.append(el("b", null, "내 위치를 받지 못했어요"), text);
  if (retry) {
    const b = el("button", "tl-ghost", "위치 다시 요청");
    b.type = "button";
    b.onclick = retry;
    note.append(b);
  }
  st.msg.replaceChildren(note);
}

// 고른(또는 가장 가까운) 곳을 코스로: 원 강조 + 내 위치에서 보라 선
function setTarget(st, it) {
  if (st.target) st.target.node.classList.remove("tl-on");
  st.target = it;
  if (it) it.node.classList.add("tl-on");
  st.course.setPath(it && st.mePos ? [st.mePos, it.pos] : []);
}

function renderList(st) {
  if (st.selected) return renderCard(st);
  const bounds = st.map.getBounds();
  const visible = st.items.filter((it) => bounds.contain(it.pos));
  st.count.textContent = "지금 지도에 보이는 화장실 " + visible.length + "곳";
  if (!visible.length) {
    const box = el("div", "tl-empty");
    const zoom = el("button", "tl-ghost", "지도 넓게 보기");
    zoom.type = "button";
    zoom.onclick = () => st.map.setLevel(st.map.getLevel() + 2);
    box.append(el("div", "tl-ring"), el("p", null, "이 화면엔 조건에 맞는 곳이 없어요"),
      el("small", null, "지도를 넓히거나 필터를 하나 풀어 보세요"), zoom);
    st.body.replaceChildren(box);
    return;
  }
  const near = st.mePos != null;
  const th = el("div", "tl-th");
  th.append(el("span", null, "번"), el("span", null, "화장실"), el("span", null, "기호"), el("span", null, near ? "도보(약)" : "구"));
  const ul = el("ul", "tl-list");
  ul.append(...visible.map((it) => {
    const b = el("button", "tl-row" + (it === st.target ? " tl-on" : ""));
    b.type = "button";
    b.append(el("span", "tl-no", String(it.n)), el("span", "tl-name", it.t.name), syms(it.t));
    if (near && it.t.dist != null) {
      const m = el("span", "tl-min", minutes(it.t.dist) + "분");
      m.append(el("small", null, meters(it.t.dist)));
      b.append(m);
    } else {
      b.append(el("span", "tl-gu", it.t.gu));
    }
    b.onclick = () => st.pick(it, true);
    const li = el("li");
    li.append(b);
    return li;
  }));
  st.body.replaceChildren(th, ul);
}

function renderCard(st) {
  const t = st.selected.t;
  st.count.textContent = "고른 화장실";
  const card = el("article", "tl-card");
  const h = el("h3");
  h.append(el("span", "tl-num", String(st.selected.n)), el("span", "tl-cname", t.name));
  if (st.mePos && t.dist != null) h.append(el("span", "tl-cmin", minutes(t.dist) + "분"));
  const kv = (k, v, extra) => {
    const r = el("div", "tl-kv");
    const x = el("span");
    if (extra) x.append(...extra);
    r.append(el("span", null, k), el("span", null, v), x);
    return r;
  };
  const go = el("a", "tl-go", "카카오맵으로 길찾기");
  go.href = "https://map.kakao.com/link/to/" + encodeURIComponent(t.name) + "," + t.lat + "," + t.lng;
  go.target = "_blank";
  go.rel = "noopener";
  const wc = el("span");
  if (t.wc) wc.innerHTML = WC;
  card.append(h,
    kv("위치", t.addr, st.mePos && t.dist != null ? [meters(t.dist)] : null),
    kv("개방", t.hours, [sym(t.kind), t.kind]),
    kv("장애인용", t.wc ? "대변기 있음" : "정보 없음", t.wc ? [wc] : null),
    go);
  const back = el("button", "tl-ghost", "목록으로");
  back.type = "button";
  back.onclick = () => { st.selected = null; renderList(st); };
  st.body.replaceChildren(card, back, el("p", "tl-caveat", "개방시간은 데이터 기준일 정보예요. 현장 사정과 다를 수 있어요."));
}

export default function ({ parentElement, data, setStateValue }) {
  const mapEl = parentElement.querySelector(".tl-map");
  const st = mapEl.__tl || (mapEl.__tl = {
    count: parentElement.querySelector(".tl-count"),
    body: parentElement.querySelector(".tl-body"),
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
      st.course = new kakao.maps.Polyline({ map: st.map, path: [], strokeWeight: 4, strokeColor: "#7B2CBF", strokeOpacity: .9 });
      kakao.maps.event.addListener(st.map, "idle", () => {
        mapEl.classList.toggle("tl-far", st.map.getLevel() >= 6);
        renderList(st);
      });
      // 화면 폭이 바뀌면(모바일 회전 등) 지도 크기를 다시 계산한다
      new ResizeObserver(() => { const c = st.map.getCenter(); st.map.relayout(); st.map.setCenter(c); }).observe(mapEl);
      st.pick = (it, pan) => {
        st.selected = it;
        setTarget(st, it);
        if (pan) st.map.panTo(it.pos);
        renderList(st);
        setStateValue("picked", { name: it.t.name, lat: it.t.lat, lng: it.t.lng });
      };
    }
    (st.items || []).forEach((it) => it.overlay.setMap(null));
    st.selected = null;
    st.target = null;
    st.mePos = data.me ? LL(data.me) : null;
    st.items = data.toilets.map((t, i) => {
      const it = { t, n: i + 1, pos: LL([t.lat, t.lng]) };
      it.node = el("div", "tl-ctl");
      it.node.title = t.name;
      it.node.append(el("b", null, String(it.n)));
      it.node.onclick = () => st.pick(it, false);
      it.overlay = new kakao.maps.CustomOverlay({ map: st.map, position: it.pos, content: it.node, clickable: true, zIndex: 2 });
      return it;
    });

    if (st.meDot) st.meDot.setMap(null);
    st.meDot = st.mePos && new kakao.maps.CustomOverlay({ map: st.map, position: st.mePos, yAnchor: .6, zIndex: 3,
      content: '<div class="tl-me" title="내 위치"></div>' });
    // 위치가 있으면 가장 가까운 곳(표의 1번)까지 미리 코스를 긋는다
    setTarget(st, st.mePos ? st.items[0] : null);
    if (st.me !== prevMe && data.me) {
      // 내 위치를 크게 확대하되, 가까운 3곳은 화면에 들어오게 (한 곳이 닫혀 있을 수도 있으니)
      st.map.setCenter(st.mePos);
      st.map.setLevel(2);
      const nearest = st.items[Math.min(2, st.items.length - 1)];
      while (nearest && !st.map.getBounds().contain(nearest.pos) && st.map.getLevel() < 8) {
        st.map.setLevel(st.map.getLevel() + 1);
      }
    } else if (!data.me && st.items.length) {
      // 위치가 없으면 조건에 맞는 곳이 모두 보이게
      const b = new kakao.maps.LatLngBounds();
      st.items.forEach((it) => b.extend(it.pos));
      st.map.setBounds(b);
    }
    renderList(st);
  }, () => { st.msg.replaceChildren(el("p", "tl-note", "지도를 불러오지 못했어요. 잠시 후 새로고침해 주세요.")); });
}
"""

_component = st.components.v2.component("toilet_map", html=HTML, css=CSS, js=JS, isolate_styles=False)


def toilet_map(js_key, df, me=None):
    """df(이름·주소·구·위도·경도·개방시간·개방구분·장애인용, 선택: 거리) 앞 200곳을 지도와 범례 표로 그린다.

    me: (위도, 경도) 현재 위치. 주면 그 주변을 크게 확대하고 가장 가까운 곳까지 코스 선을 긋는다.
    돌려주는 값: pos(브라우저가 준 현재 위치), picked(표·원에서 고른 화장실의 이름·위도·경도).
    """
    rows = df.head(MAX_MARKERS)
    toilets = [
        {
            "lat": float(r["위도"]),
            "lng": float(r["경도"]),
            "name": str(r["이름"]),
            "addr": str(r["주소"]),
            "gu": str(r["구"]),
            "kind": str(r["개방구분"]),
            "wc": bool(r["장애인용"]),
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
