import streamlit as st
import os, json, glob
from pathlib import Path

st.set_page_config(
    page_title="위험물탱크 E-매뉴얼",
    page_icon="📘",
    layout="centered",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# ======================= 데이터 (매뉴얼 목차와 동일) ======================= #
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

if "favorites" not in st.session_state: st.session_state.favorites = set()
if "history" not in st.session_state: st.session_state.history = []

def go_page(p):
    st.switch_page("pages/1_E_매뉴얼.py")  # 목차 페이지로 이동
    st.session_state.history.insert(0, p)
    st.session_state.history = st.session_state.history[:5]

# ======================= 공통 CSS ======================= #
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}
.main-title { font-size: 2.0rem; font-weight: 800; color: #222222;
              line-height: 1.4; text-align:center;}
.sub-title  { font-size: 2.0rem; font-weight: 800; color: #444444;
              line-height: 1.4; text-align:center;}
.guide-text { text-align: center; font-size: 1.1rem; margin-top: 10px; color: #555555; }

/* 파란 버튼 공통 스타일 */
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac;
    color: white;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
}
.stButton button:hover { background-color: #0072e0; }

/* 사이드바 버튼 */
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
</style>
""", unsafe_allow_html=True)

# ======================= 사이드바 ======================= #
with st.sidebar:
    st.header("📂 빠른 메뉴")
    # ✅ 대제목 → 하위 메뉴 펼침
    for main, subs in sections.items():
        with st.expander(f"📂 {main}", expanded=False):
            for sub in subs:
                st.button(sub, key=f"side-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))

    # ⭐ 즐겨찾기
    if st.session_state.favorites:
        st.markdown("---")
        st.markdown("⭐ **즐겨찾기**")
        for i, f in enumerate(st.session_state.favorites):
            st.button(f, key=f"fav-{i}-{f}", on_click=go_page, args=(f,))

    # 🕘 최근 열람
    if st.session_state.history:
        st.markdown("---")
        st.markdown("🕘 **최근 열람**")
        for i, h in enumerate(reversed(st.session_state.history[-5:])):
            st.button(h, key=f"hist-{i}-{h}", on_click=go_page, args=(h,))

# ===================== 메인 페이지 ===================== #
st.markdown('<div class="main-title">클릭하며 배우는</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
st.markdown('<div class="guide-text">📘 매뉴얼 또는 💡 자주하는 질문을 선택하세요</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📘 매뉴얼 시작하기", use_container_width=True):
        st.switch_page("pages/1_E_매뉴얼.py")
with col2:
    if st.button("💡 자주하는 질문(FAQ)", use_container_width=True):
        st.switch_page("pages/2_자주하는질문.py")

cover = None
for ext in ("jpg","jpeg","png"):
    p = Path(f"images/cover.{ext}")
    if p.exists():
        cover = p
        break
if cover:
    st.markdown("---")
    st.image(str(cover), use_container_width=True, caption="E-매뉴얼 표지")
