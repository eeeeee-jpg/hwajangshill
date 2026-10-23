# DESIGN.md

> 출처: Figma `DtszAnhvxZsCXU3U7zZfeI` › 프레임 `디자인 원칙/시스템` (node `750:2337`)
> 원본 서비스(OFFDOT, 덕질 여행 앱)의 디자인 시스템에서 **재사용 가능한 기반만** 추출했다.
> 서비스 고유 요소(로고, 아티스트 이미지, 지도 핀 등)는 [제외 / 참고용](#8-제외--참고용)에 따로 분리했다.

**적용 레벨 표기**
- 🟢 **Core**: 새 프로젝트에 그대로 적용
- 🟡 **Optional**: 필요할 때 가져다 쓰거나 값만 조정해서 사용
- ⚪ **Reference**: 원본 서비스 전용, 패턴만 참고

---

## 0. 기본 원칙

- **모바일 퍼스트**: 기준 화면 폭 `402px`(iPhone 17 Pro), 좌우 여백 `20px`.
- **핑크 하나를 주 강조색으로**: 화면에서 강조는 Primary 하나만 쓴다. Secondary(시안)와 Accent Blue는 보조나 AI 기능 같은 특수 액션에만 쓴다.
- **밝은 배경 + 쿨톤 그레이**: 배경은 `#F8F9FD`, 그레이는 푸른 기가 도는 쿨 그레이 스케일을 쓴다.
- **둥근 형태**: 칩·탭·태그는 완전한 pill(`999px`), 카드와 버튼은 `12~16px` radius.
- **선택 상태 = 핑크 테두리 + Magenta 20 배경**: 모든 선택형 컴포넌트에 같은 패턴을 쓴다.

---

## 1. Color 🟢

### Brand

| Token | Hex | 용도 |
|---|---|---|
| `primary` | `#FF52A3` | 주 CTA, 활성 탭/네비, 선택 테두리, 강조 텍스트 |
| `secondary` | `#08C4F4` | 보조 강조, 그라데이션 끝점 |
| `accent-blue` | `#6DA5EF` | AI·스마트 기능 같은 특수 액션 칩 |
| `background` | `#F8F9FD` | 앱 기본 배경 (= `gray-50`) |

### Magenta scale (Primary 틴트)

| Token | Hex | 용도 |
|---|---|---|
| `magenta-80` | `#FF007F` | 진한 강조 텍스트 (태그/배지 글자) |
| `magenta-60` | `#FFB1DD` | 보조 면, 일러스트 |
| `magenta-40` | `#FFD2E7` | Primary 버튼 그림자, 비활성 핑크 면 |
| `magenta-20` | `#FFF2F9` | 선택 상태 배경, 배지 배경, 드롭다운 hover |

### Grayscale (쿨 그레이)

| Token | Hex | 대표 용도 |
|---|---|---|
| `gray-800` | `#222222` | 기본 텍스트, 타이틀 |
| `gray-700` | `#33363F` | 진한 아이콘 |
| `gray-600` | `#505462` | 본문 보조 텍스트, 비활성 네비 라벨 |
| `gray-500` | `#717686` | 설명 텍스트, 비활성 칩 텍스트 |
| `gray-400` | `#9196A8` | 캡션, placeholder, 비활성 탭, Disabled 버튼 면 |
| `gray-300` | `#D1D4E0` | 비활성 체크박스, 구분선 강조 |
| `gray-200` | `#E2E4ED` | 기본 border, 비활성 칩 배경 |
| `gray-100` | `#F0F2F9` | 연한 border, 카드 외곽선 |
| `gray-50`  | `#F8F9FD` | 배경, 인풋 배경 |
| `white`    | `#FFFFFF` | 카드, 헤더, 네비 바 |
| `black`    | `#1D1E20` | 다크 섹션 배경 (Figma 변수 `Black`) |

> Figma 변수에는 `#222222`가 `Gray 900`으로 등록되어 있지만, 컬러 시트에서는 `Gray 800`으로 표기되어 있다. 이 문서는 시트 기준(`gray-800`)을 따른다.

### Gradient 🟡

| Token | 값 | 용도 |
|---|---|---|
| `gradient-main` | `linear-gradient(180deg, #FF52A3 0%, #08C4F4 100%)` | 브랜드 히어로, 스플래시, 앱 아이콘 |
| `gradient-sub` | `linear-gradient(0deg, #FF88B8 0%, #FF005D 100%)` | 핑크 단색 강조 배너 |

### 시맨틱 매핑 (권장)

```
text/primary      → gray-800
text/secondary    → gray-500
text/tertiary     → gray-400   (caption, placeholder)
text/accent       → primary
text/on-primary   → white

surface/page      → gray-50
surface/card      → white
surface/selected  → magenta-20
surface/input     → gray-50

border/default    → gray-200
border/subtle     → gray-100
border/selected   → primary
```

---

## 2. Typography 🟢

- **Font**: `Pretendard` (한글/영문 공통). 영문 장식용으로 `Montserrat Regular 12`가 있지만 서비스 전용이라 ⚪ 참고만 한다.
- **Weights**: Regular 400 · Medium 500 · SemiBold 600 · Bold 700 · ExtraBold 800 · Black 900
- **Line-height**: 본문·UI `1.5`, 헤딩 `1.4`, 한 줄 라벨이나 배지는 `1`(leading-none)
- **Letter-spacing**: 기본 `-0.5% ~ -1%` (예: 14px → `-0.07px`, 16px → `-0.16px`, 20px → `-0.4px`)

### Scale (모바일 UI)

| Token | Size / Weight / LH | 용도 |
|---|---|---|
| `display` | 40 / Bold / 1.4 | 온보딩 대형 타이틀 |
| `title-1` | 24 / Bold / 1.4 / -0.48px | 섹션 헤딩 |
| `title-2` | 20 / Bold / 1.4 / -0.4px | 페이지 타이틀 (예: 마이 헤더 "MY") |
| `title-3` | 18 / Bold / 1.5 | 상단 헤더 타이틀 |
| `body-1-bold` | 16 / Bold / 1.5 / -0.16px | 카드 타이틀, 리스트 타이틀, 버튼 L |
| `body-1` | 16 / Regular·Medium / 1.5 | 본문, 인풋 텍스트 |
| `body-2` | 14 / Regular·Medium / 1.5 / -0.07px | 보조 본문, 드롭다운 항목 |
| `body-2-bold` | 14 / SemiBold·Bold / 1.5 | 칩 라벨, 인풋 값 |
| `caption` | 12 / Regular·Medium / 1.5 | 설명, 주소, 메타 정보 |
| `caption-bold` | 12 / Bold / 1.5 | 필터 탭 라벨, 프로필 이름 |
| `micro` | 10 / Bold·Regular / 1 | 배지/태그, 하단 네비 라벨 |

> 사용 가능한 Weight와 Size 조합 (Figma 시트 기준)
> Black 24·14 / ExtraBold 24·20·16 / Bold 40·24·20·18·16·14·12·10 / SemiBold 14·12 / Medium 16·14·12·10 / Regular 16·14·12·10

---

## 3. Spacing · Radius · Elevation 🟢

### Spacing (4px base)

`2 · 4 · 6 · 8 · 12 · 16 · 20 · 24 · 32 · 40`

| 맥락 | 값 |
|---|---|
| 화면 좌우 패딩 | `20` |
| 카드 내부 패딩 | `16 ~ 20` |
| 칩 내부 패딩 | `8 × 12` (세로 × 가로) |
| 필터 탭 패딩 | `8 × 16` |
| 배지 패딩 | `4 × 8` |
| 아이콘–텍스트 간격 | `4` (칩), `12` (인풋), `16` (리스트 버튼) |
| 칩/탭 사이 간격 | `4 ~ 8` |

### Radius

| Token | 값 | 사용처 |
|---|---|---|
| `radius-xs` | `4px` | 체크박스, 썸네일 내부 이미지, 미니 라벨 |
| `radius-sm` | `8px` | 인풋, 말풍선 라벨, 작은 카드 |
| `radius-md` | `12px` | 버튼 L, 아이콘 배경 박스, 카드, 리스트 썸네일 |
| `radius-lg` | `16px` | 선택형 카드, 리스트형 버튼, 드롭다운, 이미지 카드 |
| `radius-full` | `999px` | 칩, 탭, 태그, 배지, 검색바, 프로필 |

### Elevation (shadow)

| Token | 값 | 사용처 |
|---|---|---|
| `shadow-primary` | `0 10px 12px -2px #FFD2E7, 0 4px 6px -4px #FFD2E7` | Primary 버튼 (핑크 글로우) |
| `shadow-neutral` | `0 10px 12px -2px #DCDCDC, 0 4px 6px -4px #DCDCDC` | Disabled/Secondary 버튼 |
| `shadow-popover` | `0 10px 15px -3px rgba(0,0,0,.10), 0 4px 6px -4px rgba(0,0,0,.10)` | 드롭다운, 팝오버 |
| `shadow-card` | `0 4px 10px rgba(0,0,0,.03)` | 카드 (아주 옅게) |
| `shadow-chip` | `0 2px 1px rgba(0,0,0,.10)` | 프로필 칩 |
| `shadow-float` | `2px 2px 2.5px rgba(0,0,0,.18)` | 플로팅 라벨, 지도 마커 |

---

## 4. Iconography 🟢

- 라인 아이콘 기반(1.5px 스트로크 느낌)이고, 활성 상태는 면 채움이나 Primary 컬러로 표시한다.
- 사이즈 체계: `16` (칩·탭 내부) · `20` (인풋) · `24` (헤더·네비) · `40` (원형 액션 버튼)
- 40px 원형 액션 버튼: 흰 원 배경 + 중앙 아이콘 (뒤로, 닫기, 공유, 좋아요, 인스타, 전화)
- 원본 세트: gift, utensils, map, bed, cafe, filter, mic, search, pin, phone, calendar-check, chevron up/down, star, heart
- 새 프로젝트에서는 [Lucide](https://lucide.dev)나 Tabler 같은 라인 아이콘 세트로 대체해도 톤이 맞는다.

---

## 5. Components

### 5.1 Button 🟢

**Button L (Primary / Disabled)**
```
width: 100% (기준 362px) · padding: 16px 0 · radius: 12px
text: 16 Bold, white, center
Primary  → bg primary   + shadow-primary
Disabled → bg gray-400  + shadow-neutral
```

**List Button (아이콘 + 타이틀 + 설명)** 🟡
```
height: 80 · padding: 24 · radius: 16 · border: 1.5px
icon box: 40×40, radius 12
title: 16 Bold (-0.16px) · desc: 12 Medium gray-500 · gap 2
Default  → bg white,       border gray-100, icon box gray-50
Selected → bg magenta-20,  border primary,  icon box primary, title primary
```

**Select Card (이미지 + 라벨, 그리드 선택형)** 🟡
```
width: ~175 · padding: 20 0 · radius: 16 · gap: 6~8
image: 40×40 원형
label: 16 Medium gray-800 / sub: 12 Regular gray-500
Default  → bg white,      border 1px gray-200
Selected → bg magenta-20, border 2px primary, text primary
```

### 5.2 Chip 🟢

```
height: 32 · padding: 8 12 · radius: full · gap: 4 · icon 16
text: 14 SemiBold/Bold (-0.07px)
```
| Variant | bg | text | 비고 |
|---|---|---|---|
| Primary | `primary` | white | 흰 2px border |
| Accent | `accent-blue` | white | AI 기능 |
| Neutral | `gray-200` | `gray-500` | "+ 추가" 류 |
| Profile (default) | `#FDFDFB` | `#7F7F7F` | 22px 아바타 + `shadow-chip` |
| Profile (selected) | `#FDFDFB` | `magenta-80` | 1px `magenta-80` border |

### 5.3 Filter Tab (Pill 탭) 🟢

```
height: 32 · padding: 8 16 · radius: full · gap: 4(탭 간) · icon 16
text: 12 Bold
Active   → bg primary, text white
Inactive → bg white, border 1px gray-200, text gray-400
```

### 5.4 Text Tab (언더 포인트 탭) 🟡

```
width: 72 · text 16
Active   → 16 Bold primary + 위쪽 4px 핑크 점
Inactive → 16 Regular gray-400
```

### 5.5 Tag / Badge 🟢

| Variant | 스펙 |
|---|---|
| Badge (상태) | bg `magenta-20`, text 10 Bold `magenta-80`, padding 4 8, radius full |
| Category label | bg `magenta-20`, text 10 Bold `magenta-80`, padding 4 6, radius 4 |
| Info tag (neutral) | bg white, border 0.5px `gray-400`, text 10 Regular `gray-400`, padding 4 8, radius 12 |
| Info tag (accent) | bg `magenta-20`, border 0.5px `primary`, text 10 Regular `primary`, padding 4 8, radius 12 |

### 5.6 Input 🟢

| Variant | 스펙 |
|---|---|
| Search field | h 48, bg `gray-50`, radius 8, padding 12 16, gap 12, icon 20, placeholder 16 Regular `gray-400` |
| Filled field | h 44, bg `gray-50`, radius 8, padding 12 16, icon 16, value 14 Bold `gray-800` |
| Pill search bar | h 40, bg white, border 1px `gray-200`, radius 44(full), padding 4 16, text 16 Regular, 우측 20px 아이콘(음성 등) |

### 5.7 Checkbox · Like 🟢

```
Checkbox: 20×20, radius 4, padding 2, 체크 아이콘 16 white
  default  → bg gray-300
  selected → bg primary
Like(heart): 24px, outline(default) ↔ filled red/primary(active)
```

### 5.8 Card 🟡

공통: bg white, radius 12, border 1px `gray-100`(선택), `shadow-card`

| Variant | 구조 |
|---|---|
| **Horizontal card** | padding 20 · 좌측 썸네일 80×120 radius 12 · 카테고리 라벨 → 타이틀 16 Bold → 주소 12 `gray-400` → 메타(아이콘 16 + 10 Medium `gray-400`) · 우측 상단 하트, 하단 배지 |
| **Compact list card** | padding 16 · 썸네일 80×80 radius 8 · 타이틀 14 Bold · 주소 12 `gray-500` · 배지 row |
| **Info card** | padding 14 20 · radius 8 · 타이틀 16 Bold + 우측 배지 · 주소 14 Medium `gray-500` · 서브 12 Medium `gray-400` |
| **Image card** | 175×208 · radius 16 · 배경 이미지 + `rgba(0,0,0,.5)` multiply 오버레이 · 하단 중앙 해시태그 12 + 타이틀 14 Bold white |

### 5.9 Header 🟢

```
bg white · padding 0 20 · justify-between · 아이콘 24, 아이콘 간격 12
Main   → h 84 · 좌: 로고 · 우: 언어 선택 + 알림
Page   → h 84 · 좌: 타이틀 20 Bold primary · 우: 알림 + 설정
Detail → h 54 · 좌: 뒤로 · 중앙: 타이틀 18 Bold gray-800 · 우: 닫기
```

### 5.10 Bottom Navigation 🟢

```
h 86 · bg white · padding 20 32 · 항목 간격 80 · 항목 4개
icon 24 + label 10 (gap 8)
Active   → icon/label primary, label Bold
Inactive → icon 라인, label 10 Regular gray-600
```

### 5.11 Dropdown 🟢

**Trigger (pill select)**
```
h 28 · w 78 · bg white · border 0.5px gray-200 · radius full · padding 4.5 8.5 · gap 6
좌 아이콘 16 + 12 Medium gray-600 + chevron
```
**Menu**
```
w 120 · bg white · border 0.5px #F3F4F6 · radius 16 · shadow-popover
item: h 40 · padding 8 16 · 14 Regular gray-600
selected: bg magenta-20 · 14 Medium primary
```

### 5.12 Avatar / Profile 🟡

```
Large: 80×80 원형, border 3px — default gray-100 / selected primary
       이름 12 Bold (default gray-400 / selected primary), gap 8
Medium: 40×40 원형 (지역/카테고리 썸네일)
Small:  22×22 원형 (칩 내부)
```

### 5.13 Index (순번 배지) 🟡

```
Small: 24×24 원형, bg primary, border 2px white, 14 Bold white
Large: 30×30 원형
  default  → bg white, border 1px primary, 16 Bold primary
  selected → bg primary, border white, 16 Bold white
```

---

## 6. 토큰 코드

### CSS Variables

```css
:root {
  /* Brand */
  --color-primary: #FF52A3;
  --color-secondary: #08C4F4;
  --color-accent-blue: #6DA5EF;
  --color-background: #F8F9FD;

  /* Magenta */
  --color-magenta-80: #FF007F;
  --color-magenta-60: #FFB1DD;
  --color-magenta-40: #FFD2E7;
  --color-magenta-20: #FFF2F9;

  /* Gray */
  --color-gray-800: #222222;
  --color-gray-700: #33363F;
  --color-gray-600: #505462;
  --color-gray-500: #717686;
  --color-gray-400: #9196A8;
  --color-gray-300: #D1D4E0;
  --color-gray-200: #E2E4ED;
  --color-gray-100: #F0F2F9;
  --color-gray-50:  #F8F9FD;
  --color-white: #FFFFFF;
  --color-black: #1D1E20;

  /* Gradient */
  --gradient-main: linear-gradient(180deg, #FF52A3 0%, #08C4F4 100%);
  --gradient-sub: linear-gradient(0deg, #FF88B8 0%, #FF005D 100%);

  /* Radius */
  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 999px;

  /* Shadow */
  --shadow-primary: 0 10px 12px -2px #FFD2E7, 0 4px 6px -4px #FFD2E7;
  --shadow-neutral: 0 10px 12px -2px #DCDCDC, 0 4px 6px -4px #DCDCDC;
  --shadow-popover: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -4px rgba(0,0,0,.1);
  --shadow-card: 0 4px 10px rgba(0,0,0,.03);
  --shadow-chip: 0 2px 1px rgba(0,0,0,.1);
  --shadow-float: 2px 2px 2.5px rgba(0,0,0,.18);

  /* Type */
  --font-sans: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}
```

### Tailwind (v4 `@theme`)

```css
@import "tailwindcss";

@theme {
  --font-sans: "Pretendard", system-ui, sans-serif;

  --color-primary: #FF52A3;
  --color-secondary: #08C4F4;
  --color-accent-blue: #6DA5EF;
  --color-background: #F8F9FD;
  --color-magenta-80: #FF007F;
  --color-magenta-60: #FFB1DD;
  --color-magenta-40: #FFD2E7;
  --color-magenta-20: #FFF2F9;
  --color-gray-800: #222222;
  --color-gray-700: #33363F;
  --color-gray-600: #505462;
  --color-gray-500: #717686;
  --color-gray-400: #9196A8;
  --color-gray-300: #D1D4E0;
  --color-gray-200: #E2E4ED;
  --color-gray-100: #F0F2F9;
  --color-gray-50:  #F8F9FD;

  --radius-xs: 4px;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;

  --shadow-primary: 0 10px 12px -2px #FFD2E7, 0 4px 6px -4px #FFD2E7;
  --shadow-neutral: 0 10px 12px -2px #DCDCDC, 0 4px 6px -4px #DCDCDC;
  --shadow-popover: 0 10px 15px -3px rgb(0 0 0 / .1), 0 4px 6px -4px rgb(0 0 0 / .1);
  --shadow-card: 0 4px 10px rgb(0 0 0 / .03);
}
```

---

## 7. 사용 규칙 (AI/개발 가이드)

1. 색상·radius·shadow는 **반드시 위 토큰만** 사용한다. 임의의 hex 값을 쓰지 않는다.
2. 한 화면의 Primary 버튼은 **하나**만 둔다. 보조 액션은 Neutral chip이나 텍스트 버튼으로 처리한다.
3. 선택 상태는 항상 `border primary + bg magenta-20 + text primary` 조합으로 표시한다.
4. 텍스트 위계는 `gray-800 → gray-500 → gray-400` 세 단계만 쓴다.
5. 상태 배지(재고, 대기 등)는 `magenta-20` 배경에 `magenta-80` 글자로 쓴다.
6. 그라데이션은 히어로, 스플래시, 브랜드 영역에만 쓰고 일반 UI 컴포넌트에는 쓰지 않는다.
7. 아이콘 크기는 16 / 20 / 24 / 40 중에서만 고른다.

---

## 8. 제외 / 참고용 ⚪

원본 서비스(OFFDOT) 전용 요소라 새 프로젝트에는 옮기지 않았다.

- **로고 / 워드마크 / 앱 아이콘**: OFFDOT 브랜드 자산
- **Montserrat** 영문 서체: 로고와 장식용
- **슬로건 카피**: "오프라인 덕질의 모든 지점을 연결하고…"
- **Map Pin / Place Marker**: 지도 기반 서비스 전용. 물방울 모양 마커(28px, `radius 20 20 20 0`, 45° 회전, `shadow-float`) + 말풍선 라벨(white, radius 8, 12 SemiBold) 패턴만 참고한다.
- **아티스트 프로필 이미지, 지역 썸네일 이미지**: 콘텐츠 자산
- **SWOT_Glass**(Glass effect, radius 12), **PPT 타이포 스타일**: 포트폴리오 발표용 스타일이라 앱 UI와 무관하다.
