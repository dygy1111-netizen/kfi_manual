import streamlit as st
from pathlib import Path

st.set_page_config(page_title="위험물탱크 E-매뉴얼",
                   page_icon="📘",
                   layout="centered")

# ✅ 공통 CSS (매뉴얼과 동일)
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}
.main-title { font-size: 2.0rem; font-weight: 800; color: #222222; line-height: 1.4; text-align:center;}
.sub-title  { font-size: 2.0rem; font-weight: 800; color: #444444; line-height: 1.4; text-align:center;}
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

/* 사이드바 고정 메뉴 스타일 */
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
.sidebar-btn button:hover {
    background-color: #0072e0 !important;
}
</style>
""", unsafe_allow_html=True)

# ===================== 사이드바 (상단 고정 메뉴만 표시) ===================== #
with st.sidebar:
    st.markdown('<div class="sidebar-btn">', unsafe_allow_html=True)

    # ✅ 버튼 클릭 시 바로 이동
    if st.button("🏠 Home", key="sb-home", use_container_width=True):
        st.switch_page("home.py")

    if st.button("📘 E 매뉴얼", key="sb-manual", use_container_width=True):
        st.switch_page("pages/1_E_매뉴얼.py")

    if st.button("💡 자주하는 질문", key="sb-faq", use_container_width=True):
        st.switch_page("pages/2_자주하는질문.py")

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== 메인 페이지 ===================== #
st.markdown('<div class="main-title">클릭하며 배우는</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
st.markdown('<div class="guide-text">📘 매뉴얼 또는 💡 자주하는 질문을 선택하세요</div>', unsafe_allow_html=True)

# 메인 버튼 (매뉴얼 시작하기 / 자주하는 질문)
col1, col2 = st.columns(2)
with col1:
    if st.button("📘 매뉴얼 시작하기", use_container_width=True):
        st.switch_page("pages/1_E_매뉴얼.py")
with col2:
    if st.button("💡 자주하는 질문(FAQ)", use_container_width=True):
        st.switch_page("pages/2_자주하는질문.py")

# 커버 이미지
cover = None
for ext in ("jpg", "jpeg", "png"):
    p = Path(f"images/cover.{ext}")
    if p.exists():
        cover = p
        break
if cover:
    st.markdown("---")
    st.image(str(cover), use_container_width=True, caption="E-매뉴얼 표지")
