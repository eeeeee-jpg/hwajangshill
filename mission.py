"""아바타 미션: 필터를 고르고 목록에서 화장실을 선택하면 미션 완료.

진행 중에는 캐릭터가 화면을 뛰어다니고, 완료되면 제자리에서 웃는다.
(빨간 배경 알람은 #23에서 뺐다: 화면을 차분하게)
시안: design/mission-prototype.html
"""
import base64
import html

import streamlit as st

# 똥 모양 커서 (32×32, 맨 위 끝이 클릭 지점)
CURSOR = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32' "
    "viewBox='0 0 32 32'%3E%3Cg fill='%238B5A2B' stroke='%234A2E14' stroke-width='1.5' "
    "stroke-linejoin='round'%3E%3Cellipse cx='16' cy='25.5' rx='13' ry='5'/%3E%3Cellipse cx='16' "
    "cy='18.5' rx='10' ry='4.6'/%3E%3Cellipse cx='16' cy='12.5' rx='7' ry='3.8'/%3E%3Cpath "
    "d='M15 3c4 2 5 5 2 8h-4c-1-3 3-4 2-8z'/%3E%3C/g%3E%3Ccircle cx='12.5' cy='18' r='2.2' "
    "fill='%23fff'/%3E%3Ccircle cx='19.5' cy='18' r='2.2' fill='%23fff'/%3E%3Ccircle cx='12.8' "
    "cy='18.3' r='1' fill='%23222'/%3E%3Ccircle cx='19.8' cy='18.3' r='1' fill='%23222'/%3E%3Cpath "
    "d='M12.5 24q3.5 2.6 7 0' fill='none' stroke='%234A2E14' stroke-width='1.4' "
    "stroke-linecap='round'/%3E%3C/svg%3E\") 15 3, auto"
)

# 페이지 공통: 커서 (배경은 테마 색 그대로)
BASE_CSS = f"""
<style>
.stApp, .stApp * {{ cursor: {CURSOR} !important; }}
[data-testid="stHeader"] {{ background: transparent; }}
</style>
"""

CHARACTER_CSS = """
<style>
.tm-runner {
  --w: 96px; --h: 116px;
  position: fixed; z-index: 999990;
  width: var(--w); height: var(--h);
  left: 2vw; top: 12vh;
  pointer-events: none;
  animation: tm-roam 16s linear infinite;
}
@keyframes tm-roam {
  0%   { left: calc((100vw - var(--w)) * .02); top: calc((100vh - var(--h)) * .12); }
  20%  { left: calc((100vw - var(--w)) * .96); top: calc((100vh - var(--h)) * .30); }
  40%  { left: calc((100vw - var(--w)) * .70); top: calc((100vh - var(--h)) * .92); }
  60%  { left: calc((100vw - var(--w)) * .06); top: calc((100vh - var(--h)) * .70); }
  80%  { left: calc((100vw - var(--w)) * .45); top: calc((100vh - var(--h)) * .45); }
  100% { left: calc((100vw - var(--w)) * .02); top: calc((100vh - var(--h)) * .12); }
}
.tm-flip { width: 100%; height: 100%; animation: tm-face 16s steps(1, end) infinite; }
@keyframes tm-face {
  0% { transform: scaleX(1); } 20% { transform: scaleX(-1); }
  60% { transform: scaleX(1); } 80% { transform: scaleX(-1); } 100% { transform: scaleX(-1); }
}
.tm-bubble {
  position: absolute; bottom: 112px; left: 50%; transform: translateX(-50%);
  white-space: nowrap; font-size: 12px; font-weight: 700; color: #FF007F;
  background: #FFFFFF; border: 1px solid #E2E4ED; border-radius: 8px; padding: 3px 8px;
  box-shadow: 2px 2px 2.5px rgba(0,0,0,.12);
}
.tm-runner img { width: 100%; height: 100%; display: block; }
.tm-done.tm-runner, .tm-done .tm-flip { animation-play-state: paused; }
.tm-done .tm-bubble { color: #FF52A3; border-color: #FF52A3; }

@media (max-width: 720px) { .tm-runner { --w: 72px; --h: 87px; } }
@media (prefers-reduced-motion: reduce) {
  .tm-runner, .tm-flip { animation: none !important; }
  .tm-runner { left: auto; top: auto; right: 16px; bottom: 16px; }
}

/* 미션 체크리스트 */
.tm-panel {
  display: flex; flex-wrap: wrap; align-items: center; gap: 10px 24px;
  background: #FFFFFF; border: 1.5px solid #F0F2F9; border-radius: 16px; padding: 14px 20px;
}
.tm-panel.tm-clear { border-color: #FF52A3; }
.tm-title { font-size: 14px; font-weight: 700; color: #717686; }
.tm-step { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #717686; }
.tm-step.tm-ok { color: #222222; font-weight: 700; }
.tm-check {
  width: 20px; height: 20px; border-radius: 4px; background: #D1D4E0;
  display: inline-flex; align-items: center; justify-content: center;
}
.tm-ok .tm-check { background: #FF52A3; }
.tm-ok .tm-check::after {
  content: ""; width: 5px; height: 9px; margin-top: -2px;
  border: solid #FFFFFF; border-width: 0 2px 2px 0; transform: rotate(45deg);
}
.tm-found { display: grid; gap: 2px; padding: 10px 12px; border-radius: 12px; background: #FFF2F9; }
.tm-found strong { font-size: 14px; color: #222222; }
.tm-found span { font-size: 12px; color: #717686; }
</style>
"""

# st.html은 인라인 SVG를 지우므로, 캐릭터는 <img>용 SVG 파일로 만들고 동작도 SVG 안에 넣는다
SVG_STYLE = """<style>
.tm-leg-f, .tm-leg-b { transform-origin: 50px 84px; }
.tm-arm-f, .tm-arm-b { transform-origin: 50px 61px; }
.tm-happy { display: none; }
.run .tm-bob { animation: bob .36s ease-in-out infinite; }
.run .tm-leg-f { animation: swing .36s ease-in-out infinite alternate; }
.run .tm-leg-b { animation: swing .36s ease-in-out infinite alternate-reverse; }
.run .tm-arm-f { animation: arm .36s ease-in-out infinite alternate-reverse; }
.run .tm-arm-b { animation: arm .36s ease-in-out infinite alternate; }
.run .tm-drop { opacity: 0; animation: drip 1s ease-out infinite; }
.run .tm-d2 { animation-delay: .33s; }
.run .tm-d3 { animation-delay: .66s; }
.happy .tm-arm-f { transform: rotate(-155deg); }
.happy .tm-arm-b { transform: rotate(155deg); }
.happy .tm-bob { animation: hop 1.2s ease-in-out infinite; }
.happy .tm-drop, .happy .tm-worried { display: none; }
.happy .tm-happy { display: inline; }
@keyframes swing { from { transform: rotate(-32deg); } to { transform: rotate(32deg); } }
@keyframes arm { from { transform: rotate(-45deg); } to { transform: rotate(45deg); } }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
@keyframes hop { 0%, 100% { transform: translateY(0); } 40% { transform: translateY(-5px); } }
@keyframes drip {
  0% { opacity: 0; transform: translate(0, 0); } 20% { opacity: 1; }
  100% { opacity: 0; transform: translate(-10px, 10px); }
}
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
  .run .tm-drop { opacity: 1; }
}
</style>"""

CHARACTER_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" class="__MODE__">__STYLE__
  <g class="tm-bob">
    <g class="tm-arm-b"><rect x="46.5" y="60" width="7" height="20" rx="3.5" fill="#FFD9B8" stroke="#222" stroke-width="2"/></g>
    <g class="tm-leg-b">
      <rect x="45.5" y="82" width="9" height="17" rx="3.5" fill="#4A82CF" stroke="#222" stroke-width="2"/>
      <rect x="44" y="97" width="15" height="7" rx="3.5" fill="#222"/>
    </g>
    <rect x="37" y="55" width="26" height="28" rx="9" fill="#FFE066" stroke="#222" stroke-width="2"/>
    <path d="M40 66 h20 v12 a6 6 0 0 1 -6 6 h-8 a6 6 0 0 1 -6 -6 z" fill="#6DA5EF" stroke="#222" stroke-width="2"/>
    <path d="M42 56 L43 67 M58 56 L57 67" stroke="#4A82CF" stroke-width="3" stroke-linecap="round"/>
    <circle cx="43.5" cy="68.5" r="1.8" fill="#FFE066" stroke="#222" stroke-width="1"/>
    <circle cx="56.5" cy="68.5" r="1.8" fill="#FFE066" stroke="#222" stroke-width="1"/>
    <rect x="46" y="72" width="8" height="5" rx="1.5" fill="none" stroke="#4A82CF" stroke-width="1.4"/>
    <g class="tm-leg-f">
      <rect x="45.5" y="82" width="9" height="17" rx="3.5" fill="#6DA5EF" stroke="#222" stroke-width="2"/>
      <rect x="44" y="97" width="15" height="7" rx="3.5" fill="#222"/>
    </g>
    <circle cx="52" cy="36" r="17" fill="#FFD9B8" stroke="#222" stroke-width="2"/>
    <circle cx="42.5" cy="38" r="4" fill="#FFD9B8" stroke="#222" stroke-width="2"/>
    <path d="M36 39 q2 6 6 8" fill="none" stroke="#6B4A2E" stroke-width="3" stroke-linecap="round"/>
    <path d="M35 32 A17 17 0 0 1 69 32 Q52 28 35 32 Z" fill="#FF52A3" stroke="#222" stroke-width="2" stroke-linejoin="round"/>
    <path d="M37 31 L20 33.5 Q17.5 35.5 21 37 L38 35 Z" fill="#FF007F" stroke="#222" stroke-width="2" stroke-linejoin="round"/>
    <path d="M58 28.6 h6" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
    <circle cx="52" cy="19.5" r="2.2" fill="#FF007F" stroke="#222" stroke-width="1.5"/>
    <circle cx="66" cy="43" r="2.8" fill="#FFB1DD"/>
    <g class="tm-worried">
      <path d="M54 33.5 L59 32 M62.5 32 L67 33.5" stroke="#222" stroke-width="1.8" stroke-linecap="round"/>
      <circle cx="57" cy="38" r="1.9" fill="#222"/>
      <circle cx="64.5" cy="38" r="1.9" fill="#222"/>
      <ellipse cx="61.5" cy="46" rx="2.8" ry="2.4" fill="#8B3A3A"/>
    </g>
    <g class="tm-happy">
      <path d="M54 39 Q57 35 60 39 M62 39 Q65 35 68 39" fill="none" stroke="#222" stroke-width="1.9" stroke-linecap="round"/>
      <path d="M56.5 43.5 Q62 51 67.5 43.5 Z" fill="#8B3A3A" stroke="#222" stroke-width="1.4" stroke-linejoin="round"/>
    </g>
    <path class="tm-drop" d="M36 22 c2.5 4 3.5 6 0 8 c-3.5 -2 -2.5 -4 0 -8z" fill="#8FD3F4"/>
    <path class="tm-drop tm-d2" d="M30 30 c2 3.2 2.8 4.8 0 6.4 c-2.8 -1.6 -2 -3.2 0 -6.4z" fill="#8FD3F4"/>
    <path class="tm-drop tm-d3" d="M72 24 c2 3.2 2.8 4.8 0 6.4 c-2.8 -1.6 -2 -3.2 0 -6.4z" fill="#8FD3F4"/>
    <g class="tm-arm-f">
      <rect x="46.5" y="60" width="7" height="20" rx="3.5" fill="#FFD9B8" stroke="#222" stroke-width="2"/>
      <rect x="45.5" y="57" width="9" height="7" rx="3" fill="#FFE066" stroke="#222" stroke-width="2"/>
    </g>
  </g>
</svg>
"""


def _character_src(mode):
    svg = CHARACTER_SVG.replace("__MODE__", mode).replace("__STYLE__", SVG_STYLE)
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


RUN_SRC = _character_src("run")
HAPPY_SRC = _character_src("happy")


def _step(label, ok):
    return f'<div class="tm-step{" tm-ok" if ok else ""}"><span class="tm-check"></span>{label}</div>'


def _panel_html(filter_changed, selected):
    done = filter_changed and selected is not None
    found = ""
    if done:
        meta = f"{selected['주소']} · {selected['개방시간'] if str(selected['개방시간']) != 'nan' else '개방시간 정보없음'}"
        if selected["장애인용"]:
            meta += " · 장애인용 있음"
        found = (
            f'<div class="tm-found"><strong>{html.escape(str(selected["이름"]))}</strong>'
            f"<span>{html.escape(meta)}</span></div>"
        )
    return (
        f'<div class="tm-panel{" tm-clear" if done else ""}">'
        '<span class="tm-title">미션</span>'
        f'{_step("① 조건 고르기", filter_changed)}'
        f'{_step("② 목록에서 화장실 선택", selected is not None)}'
        f"{found}</div>"
    )


def render(slot, filter_changed, selected):
    """미션 패널을 slot에 그리고(slot이 None이면 생략), 캐릭터와 배경 CSS를 페이지에 넣는다.

    filter_changed: 필터가 하나라도 기본값에서 바뀌었는지
    selected: 목록에서 고른 행(pd.Series) 또는 None
    """
    done = filter_changed and selected is not None
    st.html(CHARACTER_CSS)
    if slot is not None:  # None이면 체크리스트 패널 없이 캐릭터·배경만
        slot.html(_panel_html(filter_changed, selected))

    bubble = "찾았다!" if done else "화장실 어디야?!"
    st.html(
        f'<div class="tm-runner{" tm-done" if done else ""}">'
        f'<div class="tm-bubble">{bubble}</div>'
        f'<div class="tm-flip"><img src="{HAPPY_SRC if done else RUN_SRC}" '
        'alt="거꾸로 쓴 야구모자와 멜빵바지 차림의 어린이 캐릭터"></div></div>'
    )
    st.html(BASE_CSS)
