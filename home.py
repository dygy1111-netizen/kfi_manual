import streamlit as st

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="wide")

# ───── 공공기관 스타일 CSS ─────
st.markdown("""
<style>
.title {text-align:center; font-size:2.2rem; font-weight:800; color:#003366; margin-bottom:1.2em;}
.subtitle {text-align:center; font-size:1.2rem; color:#333333; margin-bottom:1.5em;}
.menu-title {font-size:1.1rem; font-weight:600; margin-top:1.5em;}
</style>
""", unsafe_allow_html=True)

# ───── 메인 타이틀 ─────
st.markdown('<div class="title">📘 클릭하며 배우는 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">왼쪽 상단 메뉴(☰)를 열거나 아래 링크를 클릭해 원하는 페이지로 이동하세요.</div>',
            unsafe_allow_html=True)

# ───── 목차(간단 링크) ─────
st.markdown('<div class="menu-title">📑 주요 항목 바로가기</div>', unsafe_allow_html=True)

st.markdown("- [1.1 안전거리](1_위험물탱크%20위치_구조_설비%20기준/1_안전거리)")
st.markdown("- [1.2 보유공지](1_위험물탱크%20위치_구조_설비%20기준/2_보유공지)")
st.markdown("- [FAQ (자주하는 질문)](5_자주하는질문)")
