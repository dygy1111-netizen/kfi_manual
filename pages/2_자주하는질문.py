import streamlit as st
import json, re
from pathlib import Path

# ======================= 기본 설정 ======================= #
st.set_page_config(page_title="자주하는 질문", page_icon="💡", layout="centered")

# ======================= 목차 데이터 (매뉴얼 동일) ======================= #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리","1.2 보유공지","1.3 표지 및 게시판",
        "1.4-1 탱크 내부 압력 해소 구조","1.4-2 탱크 부식방지 설비","1.4-3 통기관",
        "1.4-4 자동계량식 유량계","1.4-5 주입구","1.4-6 펌프설비",
        "1.4-7 배관 및 밸브","1.4-8 부상지붕탱크의 설비",
        "1.4-9 전기설비","1.4-10 부속설비",
        "1.5 방유제","1.6 옥외탱크저장소의 특례",
        "1.7 소화설비","1.8 경보설비"
    ],
    "2. 안전성능검사": ["2.1 검사절차 및 확인사항","2.2 검사방법","2.3 참고사항"],
    "3. 정기검사": ["3.1 검사절차 및 확인사항","3.2 검사방법","3.3 참고사항"],
    "4. 부록": [
        "물분무설비 설치기준","부상지붕탱크 구조",
        "내부부상지붕탱크 구조","전기방식설비",
        "위험물제조소등 접지저항기준(소방청 협의사항)"
    ]
}

if "page" not in st.session_state:
    st.session_state.page = "자주하는 질문"

def go_page(p):
    st.session_state.page = p

# ======================= CSS (매뉴얼 동일 스타일) ======================= #
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}
.main-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #222222;
    line-height: 1.4;
    text-align: center;
}
/* 공통 버튼 */
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac;
    color: white;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
    transition: background-color 0.2s ease;
}
.stButton button:hover { background-color: #0072e0; }

/* 사이드바 빠른 이동 버튼 */
.sidebar-btn button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac !important;
    color: white !important;
    border: none;
    padding: 0.6em;
    font-size: 1rem;
    font-weight: 600;
}
.sidebar-btn button:hover { background-color: #0072e0 !important; }

/* FAQ 카드 */
details.faq {
  border: 2px solid #d0d7e2;
  border-radius: 10px;
  padding: 0.7rem 1rem;
  margin: 0.8rem 0;
  background: #f8fbff;        /* 💡 매뉴얼 표와 비슷한 연한 파랑 */
  transition: box-shadow 0.2s ease;
}
details.faq[open] {
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
details.faq summary {
  list-style: none;
  cursor: pointer;
  font-weight: 700;
  font-size: 1.05rem;
  color: #003366;             /* 💡 매뉴얼과 동일한 진한 파랑 */
  outline: none;
  padding: 0.3rem 0;
}
details.faq summary::-webkit-details-marker { display: none; }
details.faq summary:after {
  content: "▾";
  float: right;
  transition: transform 0.2s ease;
  color: #005bac;
}
details.faq[open] summary:after { transform: rotate(180deg); }

details.faq div {
  margin-top: 0.6rem;
  color: #333333;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* 검색 하이라이트 */
mark {
  padding: 0 2px;
  background: #fff59d;
  border-radius: 3px;
}
</style>
""", unsafe_allow_html=True)

# ======================= 사이드바 ======================= #
with st.sidebar:
    st.header("📂 빠른 메뉴")
    for main, subs in sections.items():
        with st.expander(f"📂 {main}", expanded=False):
            for sub in subs:
                st.button(sub, key=f"side-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))

# ======================= FAQ 데이터 ======================= #
faq_path = Path("faq.json")
if faq_path.exists():
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_list = json.load(f)
else:
    faq_list = [
        {"q": "샘플 질문", "a": "샘플 답변입니다.\n\n![](faq_images/sample.jpg)"}
    ]

# ======================= 검색 ======================= #
st.markdown('<div class="main-title">💡 자주하는 질문 (FAQ)</div>', unsafe_allow_html=True)
keyword = st.text_input("🔍 검색어를 입력하세요", placeholder="질문 또는 답변 키워드").strip()

if keyword:
    key_l = keyword.lower()
    results = [it for it in faq_list if key_l in it["q"].lower() or key_l in it["a"].lower()]
else:
    results = faq_list

def highlight(text, kw):
    if not kw:
        return text
    pattern = re.compile(re.escape(kw), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# ======================= FAQ 렌더링 ======================= #
if results:
    for item in results:
        q_html = highlight(item["q"], keyword)
        a_html = highlight(item["a"], keyword)
        st.markdown(
            f"<details class='faq'><summary>{q_html}</summary>"
            f"<div>{a_html}</div></details>",
            unsafe_allow_html=True
        )
else:
    st.warning("검색 결과가 없습니다.")
