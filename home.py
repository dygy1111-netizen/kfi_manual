import streamlit as st

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘")  # 앱 아이콘은 유지 가능

# ✅ 깔끔한 2줄 타이틀
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
</style>

<div class="title-container">
    <div class="main-title">클릭하며 배우는</div>
    <div class="sub-title">위험물탱크 E-매뉴얼</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
👈 **왼쪽 상단의 ▤ 메뉴(사이드바)** 를 클릭해  
**E-매뉴얼** 또는 **자주하는 질문(FAQ)** 페이지로 이동하세요.
""")
