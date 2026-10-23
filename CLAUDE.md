# CLAUDE.md

이 문서는 우리 조 지도 서비스의 **개발 규칙**이다.
조원과 AI(Claude Code) 모두 작업 전에 이 문서를 읽고 그대로 따른다.

---

## 1. 프로젝트 개요

**한 줄 소개**
공중화장실 공공데이터를 정리해, 조건(24시간 개방, 장애인용 등)에 맞는 화장실을 카카오 지도 위에서 바로 찾는 Streamlit 서비스.

**기술 스택**

| 구분 | 기술 |
| --- | --- |
| 언어 | Python 3.11+ |
| 데이터 처리 | pandas |
| 화면 | Streamlit |
| 지도 | 카카오 지도 JS SDK (`st.components.v1.html()`로 삽입) |
| 좌표 변환 | requests + 카카오 로컬 API (정제 단계에서만 사용) |
| 환경 변수 | python-dotenv |

**실행 방법**

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 환경 변수 파일 만들기 (.env.example 복사 후 키 입력)
cp .env.example .env

# 3. [최초 1회] 정제 (서울 원본 data/raw/seoul_toilets.csv는 레포에 포함)
python prepare_data.py

# 4. 앱 실행
streamlit run app.py
```

---

## 2. 개발 흐름 전체 그림

모든 작업은 **Issue에서 시작해서 PR 머지로 끝난다.**

```
① Issue 생성 (할 일 정의, 담당자 지정)
        ↓
② main 최신화 → 브랜치 생성 (타입/이슈번호-작업명)
        ↓
③ 작업 + 커밋 (타입: 내용 (#이슈번호))
        ↓
④ push → PR 생성 (Closes #이슈번호)
        ↓
⑤ 리뷰어 1명 리뷰 → 수정 → 승인
        ↓
⑥ main에 머지 → 원격·로컬 브랜치 삭제 → Issue 자동 닫힘
```

- 1인 1 PR 이상 필수.
- `main`에 직접 커밋하거나 push하지 않는다.
- Issue 없는 브랜치, 브랜치 없는 PR은 만들지 않는다.

---

## 3. Issue 작성 규칙

**제목 형식**

```
[타입] 작업 내용
```

예시

- `[feat] 사이드바 필터와 metric 3개 연동`
- `[data] 개방시간 분류 및 좌표 결측 채우기`
- `[docs] README 실행 방법 작성`

**본문 템플릿**

```markdown
## 목적
이 작업을 왜 하는지 한두 문장

## 할 일
- [ ] 작업 1
- [ ] 작업 2

## 완료 조건
- 어떤 상태가 되면 끝난 것인지 (예: 필터를 바꾸면 metric 숫자가 바뀐다)

## 참고
관련 문서, 스크린샷, 링크
```

- 담당자(Assignees)를 반드시 지정한다.
- 이슈 하나는 PR 하나로 끝낼 수 있는 크기로 쪼갠다.

---

## 4. 브랜치 네이밍

**형식**

```
타입/이슈번호-작업명
```

**타입**

| 타입 | 용도 | 예시 |
| --- | --- | --- |
| `feat` | 새 기능 | `feat/3-filter-metric` |
| `fix` | 버그 수정 | `fix/12-empty-filter-error` |
| `data` | 데이터 정제·스크립트 | `data/1-clean-toilets` |
| `docs` | 문서 (README, CLAUDE.md 등) | `docs/5-readme` |
| `style` | 테마·화면 스타일 | `style/6-theme-config` |
| `chore` | 설정·패키지·gitignore | `chore/2-init-setting` |

**규칙**

- 작업명은 **영어 소문자 + 하이픈**으로 2~4단어. (한글, 공백, 대문자, 밑줄 금지)
- 이슈번호는 반드시 넣는다. 브랜치 이름만 보고 어떤 이슈인지 알 수 있어야 한다.
- 브랜치 하나 = 이슈 하나. 다른 이슈 작업을 섞지 않는다.

**브랜치 만들기**

```bash
git switch main
git pull origin main
git switch -c feat/3-filter-metric
```

---

## 5. 커밋 메시지 규칙

**형식**

```
타입: 내용 (#이슈번호)
```

타입은 4번 브랜치 타입과 같다. 내용은 한글로, 무엇을 했는지 짧게 쓴다.

예시

```
feat: 개방구분 필터 추가 (#3)
feat: metric 3개 계산 및 표시 (#3)
fix: 필터 결과 0건일 때 안내 문구 표시 (#12)
data: 개방시간 24시간/시간제한/정보없음 분류 (#1)
docs: README에 실행 방법 추가 (#5)
```

- 커밋 하나에는 한 가지 변경만 담는다.
- "수정", "작업중", "asdf" 같은 의미 없는 메시지는 쓰지 않는다.

---

## 6. PR 규칙

**제목 형식**

```
[타입] 작업 내용 (#이슈번호)
```

예시: `[feat] 사이드바 필터와 metric 3개 연동 (#3)`

**본문 템플릿**

```markdown
## 관련 이슈
Closes #이슈번호

## 변경 내용
- 무엇을 바꿨는지

## 확인 방법
1. `streamlit run app.py`
2. 사이드바에서 ○○ 선택
3. metric·지도·표가 함께 바뀌는지 확인

## 스크린샷
(화면 변경이 있으면 첨부)

## 보안 체크
- [ ] `.env` 파일이 커밋에 없다
- [ ] 코드에 키 문자열이 직접 적혀 있지 않다
- [ ] REST 키가 HTML 문자열에 들어가지 않는다
- [ ] `data/raw/`에 `seoul_toilets.csv` 외의 원본 파일이 커밋에 없다
```

**리뷰와 머지**

- 리뷰어 1명을 지정하고, **승인(Approve)을 받은 뒤에만 머지**한다.
- 리뷰어는 확인 방법대로 직접 실행해 보고, 보안 체크 항목을 다시 확인한다.
- 수정 요청을 받으면 같은 브랜치에 커밋을 추가해서 push한다. (새 PR을 만들지 않는다)
- 머지는 PR 작성자가 한다.
- 머지 후 브랜치를 삭제한다.

**리뷰 짝**

| PR 작성자 | 리뷰어 |
| --- | --- |
| A (데이터) | C |
| B (지도) | A |
| C (화면 연동·문서) | B |
| D (디자인·README) | C |

**머지 순서**

컬럼 약속에 의존하는 순서대로 머지하면 충돌이 적다.

```
A (데이터) → B (지도) → C (화면 연동) → D (README·테마)
```

---

## 7. 브랜치 최신화와 충돌 처리

**작업 시작 전, PR 올리기 전에 main을 반영한다.**

```bash
git switch main
git pull origin main
git switch feat/3-filter-metric
git merge main
```

**충돌이 났을 때**

1. 충돌 난 파일을 열어 `<<<<<<<`, `=======`, `>>>>>>>` 표시를 찾는다.
2. 내 코드와 main 코드 중 맞는 쪽을 남기거나 합친다. 남의 담당 코드라면 **담당자에게 물어보고** 결정한다.
3. 표시를 모두 지운 뒤 실행해서 동작을 확인한다.
4. 커밋하고 push한다.

```bash
git add .
git commit -m "chore: main 병합 충돌 해결 (#3)"
git push
```

- `git push --force`는 사용하지 않는다.

---

## 8. 보안 규칙

| 규칙 | 이유 |
| --- | --- |
| `.env`는 절대 커밋하지 않는다 | 키 유출 방지 |
| 코드에 키를 직접 쓰지 않는다. `os.getenv()`로 읽는다 | 키 유출 방지 |
| REST 키는 `prepare_data.py`에서만 사용한다 | REST 키는 서버(Python)용 |
| `components.html()`에 넣는 HTML에는 JavaScript 키만 쓴다 | HTML은 브라우저에 그대로 노출됨 |
| 원본은 서울만 잘라 `data/raw/seoul_toilets.csv`로 커밋한다. 전국 원본 등 다른 원본은 커밋하지 않는다 | 대용량 파일 금지 조건 (전국 8MB → 서울 0.5MB) |

**.gitignore 필수 항목**

```
.env
data/raw/*
!data/raw/seoul_toilets.csv
__pycache__/
.venv/
.DS_Store
._*
Thumbs.db
desktop.ini
```

**.env.example** (키 이름만, 값은 비워서 커밋)

```
KAKAO_REST_API_KEY=
KAKAO_JS_KEY=
```

**PR 전 확인 명령어**

```bash
# 커밋 예정 파일 목록에 .env, 전국 원본이 없는지 확인
git status

# 코드에 키 문자열이 남아 있는지 확인 (결과가 os.getenv 줄만 나와야 함)
git grep -n "KAKAO"
```

---

## 9. 코드 규칙

**파일별 역할**

| 파일 | 역할 | 담당 |
| --- | --- | --- |
| `prepare_data.py` | 원본 → 정제 CSV 생성 (카카오 REST API 사용, 1회 실행) | A |
| `map_view.py` | df를 받아 카카오 지도 HTML 문자열을 만드는 함수 | B |
| `app.py` | Streamlit 진입점: 필터, metric, 지도, 표, 출처 표시 | C |
| `.streamlit/config.toml` | 테마 색상 | D |
| `README.md` | 소개, 실행 방법, 출처 | D |

**정제 CSV 컬럼 약속** — `data/toilets_clean.csv`

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `이름` | str | 화장실명 |
| `주소` | str | 도로명 우선, 없으면 지번 |
| `구` | str | 시군구 |
| `위도` | float | WGS84 |
| `경도` | float | WGS84 |
| `개방시간` | str | 원본 텍스트 그대로 |
| `개방구분` | str | `24시간` / `시간제한` / `정보없음` |
| `장애인용` | bool | 장애인용 대변기 1개 이상이면 True |

- 컬럼 이름·타입을 바꾸려면 **Issue를 먼저 만들고 팀 합의 후** 바꾼다.

**연동 원칙**

- `app.py`는 API를 호출하지 않는다. 정제 CSV만 읽는다. (`@st.cache_data` 사용)
- 필터 결과는 **`df_f` 하나**로 만들고, 지도·metric·표가 모두 `df_f`만 사용한다.
- 지도에는 최대 200개만 넘긴다. (`df_f.head(200)`) 200개를 넘으면 안내 문구를 표시한다.
- `df_f`가 비어 있으면 `st.info()`로 안내한다.
- 출처와 데이터 기준일을 `st.caption()`으로 표시한다. "실시간"이라는 표현은 쓰지 않는다.

---

## 10. AI(Claude Code)에게 주는 지침

Claude Code로 작업할 때는 아래를 반드시 지킨다.

- 작업 전에 **어떤 Issue의 작업인지 확인**하고, 그 이슈 범위 밖의 파일은 수정하지 않는다. 필요하면 수정하지 말고 먼저 제안한다.
- 브랜치·커밋·PR은 이 문서의 4~6번 형식을 따른다.
- `main` 브랜치에서 직접 작업하지 않는다. 현재 브랜치가 `main`이면 작업을 멈추고 알린다.
- 키 값을 코드, HTML, 커밋 메시지, PR 본문에 쓰지 않는다. 키는 `os.getenv()`로만 읽는다.
- `.env`, `data/raw/seoul_toilets.csv` 외의 원본을 커밋하지 않는다. `git add .` 전에 `git status`로 확인한다.
- 정제 CSV 컬럼 약속(9번)을 바꾸지 않는다.
- `git push --force`, `git reset --hard` 등 기록을 지우는 명령은 실행하지 않는다.
- 새 패키지가 필요하면 `requirements.txt`에 추가하고 PR 본문에 적는다.
- 코드를 바꾼 뒤에는 `streamlit run app.py`로 실행 확인 방법을 PR 본문에 적는다.
