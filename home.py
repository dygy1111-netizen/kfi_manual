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

# ===== 안내 문구 (두 줄 유지 + 이모지) =====
st.markdown("""
<div class="guide-text">
☰ <b>왼쪽 상단 메뉴</b>를 클릭해 📘 <b>E-매뉴얼</b><br>
또는 💡 <b>자주하는 질문(FAQ)</b> 페이지로 이동하세요.
</div>
""", unsafe_allow_html=True)

# ===== 하단 커버 이미지 =====
cover_path = None
for ext in ("jpg", "jpeg", "png"):
    p = Path(f"images/cover.{ext}")
    if p.exists():
        cover_path = p
        break

if cover_path:
    st.markdown("---")
    st.image(str(cover_path), use_container_width=True, caption="E-매뉴얼 표지")
else:
    st.info("💡 images 폴더에 cover.jpg/png/jpeg 파일을 넣으면 여기 표지가 표시됩니다.")
