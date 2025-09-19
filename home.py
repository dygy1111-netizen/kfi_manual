import streamlit as st

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="wide")

# ===== 스타일 유지 =====
st.markdown("""
<style>
.title-container {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
    font-family: 'Noto Sans KR', sans-serif;
}
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #003366;
    line-height: 1.4;
}
.sub-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #003366;
    line-height: 1.4;
}
.guide-text {
    text-align: center;
    font-size: 1.1rem;
    margin-top: 15px;
    line-height: 1.6;
}
.link-box {
    max-width: 600px;
    margin: 40px auto 0 auto;
    padding: 20px;
    background-color: #ffffff;
    border: 1.5px solid #d0d7e2;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
.link-box a {
    text-decoration: none;
    font-size: 1.05rem;
    color: #005bac;
    display: block;
    margin: 10px 0;
}
.link-box a:hover {
    color: #0072e0;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ===== 타이틀 =====
st.markdown("""
<div class="title-container">
    <div class="main-title">클릭하며 배우는</div>
    <div class="sub-title">위험물탱크 E-매뉴얼</div>
</div>
""", unsafe_allow_html=True)

# ===== 안내문 =====
st.markdown("""
<div class="guide-text">
☰ **왼쪽 상단 메뉴**를 클릭하거나 <br>
아래 바로가기를 눌러 원하는 페이지로 이동하세요.
</div>
""", unsafe_allow_html=True)

# ===== 주요 링크 =====
st.markdown("""
<div class="link-box">
<a href="1_위험물탱크%20위치_구조_설비 기준/1_안전거리">📑 1.1 안전거리</a>
<a href="1_위험물탱크%20위치_구조_설비 기준/2_보유공지">📑 1.2 보유공지</a>
<a href="5_자주하는질문">💡 자주하는 질문(FAQ)</a>
</div>
""", unsafe_allow_html=True)
