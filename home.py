import streamlit as st
from pathlib import Path

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="wide")

# ===== CSS =====
cover_image = Path("images/cover.jpg").as_posix()  # jpg/png 등 가능
st.markdown(f"""
<style>
/* 전체 배경 이미지 */
.stApp {{
    background: url("{cover_image}") no-repeat center center fixed;
    background-size: cover;
}}

/* 반투명 오버레이 */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.45);   /* 어두운 투명 레이어 */
    z-index: 0;
}}

/* 중앙 박스 */
.cover-container {{
    position: relative;
    z-index: 1;
    text-align: center;
    padding: 60px 20px;
    background: rgba(255,255,255,0.85);
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    max-width: 600px;
    margin: 10% auto;
    font-family: 'Noto Sans KR', sans-serif;
}}
.cover-title {{
    font-size: 2.6rem;
    font-weight: 800;
    color: #003366;
    margin-bottom: 10px;
}}
.cover-sub {{
    font-size: 1.2rem;
    color: #333333;
    margin-bottom: 30px;
}}
.cover-button > button {{
    background-color: #005bac;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.8em 2em;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
}}
.cover-button > button:hover {{
    background-color: #0072e0;
}}
</style>
""", unsafe_allow_html=True)

# ===== 본문 =====
st.markdown("""
<div class="cover-container">
    <div class="cover-title">클릭하며 배우는<br>위험물탱크 E-매뉴얼</div>
    <div class="cover-sub">위험물탱크 설비·검사·부록 정보를<br>한눈에 쉽게 학습하세요.</div>
</div>
""", unsafe_allow_html=True)

# 중앙 버튼
st.markdown('<div class="cover-button" style="text-align:center">', unsafe_allow_html=True)
if st.button("📘 E-매뉴얼 시작하기"):
    # 👉 버튼 클릭 시 사이드바 메뉴로 안내
    st.session_state.page_hint = "E-매뉴얼"  # pages/1_E_매뉴얼.py 에서 사용 가능
    st.success("왼쪽 사이드바에서 **E-매뉴얼**을 선택하세요.")
st.markdown('</div>', unsafe_allow_html=True)
