import streamlit as st

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="wide")

# ----- 스타일 유지 ----- #
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

# ----- 메인 타이틀 ----- #
st.markdown("""
<div class="title-container">
    <div class="main-title">클릭하며 배우는</div>
    <div class="sub-title">위험물탱크 E-매뉴얼</div>
</div>
""", unsafe_allow_html=True)

# ----- 안내문 ----- #
st.markdown("""
<div class="guide-text">
☰ <b>왼쪽 상단 메뉴</b>를 클릭하거나<br>
아래 항목을 선택해 바로 이동하세요.
</div>
""", unsafe_allow_html=True)

# ----- 목차 (개별 페이지 링크) ----- #
st.markdown("""
<div class="link-box">
<a href="1_안전거리">📑 1.1 안전거리</a>
<a href="2_보유공지">📑 1.2 보유공지</a>
<a href="3_표지 및 게시판">📑 1.3 표지 및 게시판</a>
<a href="4_외부구조 및 설비">📑 1.4 외부구조 및 설비</a>
<a href="5_방유제">📑 1.5 방유제</a>
<a href="6_옥외탱크저장소의 특례">📑 1.6 옥외탱크저장소의 특례</a>
<a href="7_소화설비">📑 1.7 소화설비</a>
<a href="8_검사절차 및 확인사항">📑 2.1 검사절차 및 확인사항</a>
<a href="9_검사방법">📑 2.2 검사방법</a>
<a href="10_참고사항">📑 2.3 참고사항</a>
<a href="11_정기검사 절차 및 확인사항">📑 3.1 정기검사 절차 및 확인사항</a>
<a href="12_정기검사 방법">📑 3.2 정기검사 방법</a>
<a href="13_정기검사 참고사항">📑 3.3 정기검사 참고사항</a>
<a href="14_소방청 질의회신 및 협의사항">📑 4.1 소방청 질의회신 및 협의사항</a>
<a href="15_검사관련 규격 및 기술지침">📑 4.2 검사관련 규격 및 기술지침</a>
<a href="16_검사 부적합 사례 및 실무 팁">📑 4.3 검사 부적합 사례 및 실무 팁</a>
<a href="17_자주하는질문">💡 자주하는 질문(FAQ)</a>
</div>
""", unsafe_allow_html=True)
