import streamlit as st
from pathlib import Path

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘")

# ===== 타이틀 스타일 =====
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
    margin-top: 10px;
    line-height: 1.6;
}
</style>

<div class="title-container">
    <div class="main-title">클릭하며 배우는</div>
    <div class="sub-title">위험물탱크 E-매뉴얼</div>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="centered")

st.markdown("""
<div class="title-container">
    <div class="main-title">클릭하며 배우는</div>
    <div class="sub-title">위험물탱크 E-매뉴얼</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="guide-text">
📘 <b>매뉴얼 시작하기</b> 또는 💡 <b>자주하는 질문(FAQ)</b>을 선택하세요.<br>
왼쪽 사이드바에서도 모든 메뉴를 탐색할 수 있습니다.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📘 매뉴얼 시작하기", use_container_width=True):
        st.switch_page("pages/1_E_매뉴얼.py")   # ✅ 매뉴얼로 이동
with col2:
    if st.button("💡 자주하는 질문 (FAQ)", use_container_width=True):
        st.switch_page("pages/2_자주하는질문.py")  # ✅ FAQ로 이동

# 표지 이미지
cover = None
for ext in ("jpg", "jpeg", "png"):
    p = Path(f"images/cover.{ext}")
    if p.exists():
        cover = p
        break
if cover:
    st.markdown("---")
    st.image(str(cover), use_container_width=True, caption="E-매뉴얼 표지")
else:
    st.info("💡 images 폴더에 cover.jpg/png/jpeg 파일을 넣으면 표지가 표시됩니다.")
