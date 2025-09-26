import streamlit as st
import json, re, glob, os
from pathlib import Path

st.set_page_config(page_title="자주하는 질문", page_icon="💡", layout="wide")

# ======================= 데이터 (목차 공유) ======================= #
# 👉 home.py / 1_E_매뉴얼.py 와 동일하게 유지
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
    "4. 부록": ["물분무설비 설치기준","부상지붕탱크 구조",
               "내부부상지붕탱크 구조","전기방식설비",
               "위험물제조소등 접지저항기준(소방청 협의사항)"]
}

# ======================= 세션 상태 ======================= #
if "page" not in st.session_state:
    st.session_state.page = "자주하는 질문"

def go_page(p):
    st.session_state.page = p

# ======================= 사이드바 ======================= #
with st.sidebar:
    # 💡 FAQ 고정 버튼
    st.button("💡 자주하는 질문 (현재)", use_container_width=True)

    st.markdown("---")
    st.header("📚 전체 메뉴")
    # ✅ 대제목 → 클릭 시 하위 메뉴 펼침
    for main, subs in sections.items():
        with st.expander(f"📂 {main}", expanded=False):
            for sub in subs:
                st.button(sub, key=f"side-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))

# ======================= FAQ 본문 ======================= #
st.markdown(
    "<h3 style='font-size:1.3rem; font-weight:700; margin-bottom:0.8rem;'>💡 자주하는 질문 (FAQ)</h3>",
    unsafe_allow_html=True
)

# ---------------- CSS (하이라이트 + 접기/펼치기)
st.markdown("""
<style>
details.faq {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.6rem 0.9rem;
  margin: 0.6rem 0;
  background: #ffffff;
}
details.faq[open] {
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
details.faq summary {
  list-style: none;
  cursor: pointer;
  font-weight: 700;
  font-size: 1.05rem;
  outline: none;
}
details.faq summary::-webkit-details-marker { display: none; }
details.faq summary:after {
  content: "▾";
  float: right;
  transition: transform 0.2s ease;
  color: #666;
}
details.faq[open] summary:after {
  transform: rotate(180deg);
}
mark { padding: 0 2px; background: #fff59d; }
</style>
""", unsafe_allow_html=True)

# ---------------- 데이터 로딩
faq_path = Path("faq.json")
if faq_path.exists():
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_list = json.load(f)
else:
    faq_list = [
        {"q": "샘플 질문", "a": "샘플 답변입니다.\n\n![](faq_images/sample.jpg)"}
    ]

# ---------------- 검색 입력
keyword = st.text_input("🔍 검색어를 입력하세요", placeholder="질문 또는 답변 키워드").strip()

# ---------------- 검색 필터링
if keyword:
    key_l = keyword.lower()
    results = [it for it in faq_list if key_l in it["q"].lower() or key_l in it["a"].lower()]
else:
    results = faq_list

# ---------------- 하이라이트 함수
def highlight(text, kw):
    if not kw:
        return text
    pattern = re.compile(re.escape(kw), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# ---------------- 렌더링 (질문 → 이미지 → 답변)
if results:
    for item in results:
        q_html = highlight(item["q"], keyword)
        a_html = highlight(item["a"], keyword)

        # HTML <details>로 접기/펼치기 구현
        st.markdown(
            f"<details class='faq'><summary>{q_html}</summary>"
            f"<div style='margin-top:0.6rem;'>{a_html}</div></details>",
            unsafe_allow_html=True
        )
else:
    st.warning("검색 결과가 없습니다.")
