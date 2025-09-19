import streamlit as st

st.set_page_config(page_title="E-매뉴얼", page_icon="📘", layout="wide")

# ---------- 공공기관 스타일 CSS ---------- #
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #f5f7fa;
    line-height: 1.7;
}
.big-title {
    font-size: 2.2rem !important;
    font-weight: 800;
    text-align: center;
    color: #003366;
    margin-bottom: 1.2em;
}
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac;
    color: white;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.4em;
}
.stButton button:hover { background-color: #0072e0; }
.img-box {
    background-color: #ffffff;
    border: 1.5px solid #d0d7e2;
    border-radius: 10px;
    padding: 1em;
    margin: 1.2em 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
table { width: 100%; border-collapse: collapse; margin-top: 1em; }
table th, table td { border: 1px solid #d0d7e2; padding: 8px; text-align: center; }
table th { background-color: #005bac; color: white; }
table tr:nth-child(even) { background-color: #f0f4f8; }
.back-btn button {
    background-color: #005bac;
    color: white;
    border-radius: 6px;
    padding: 0.6em 1em;
    border: none;
    font-weight: 600;
}
.back-btn button:hover { background-color: #0072e0; }
</style>
""", unsafe_allow_html=True)

# ---------- 목차 데이터 ---------- #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리 및 보유공지",
        "1.2 표지 및 게시판",
        "1.3 외부구조 및 설비",
        "1.4 방유제",
        "1.5 옥외탱크저장소의 특례",
        "1.6 소화설비"
    ],
    "2. 안전성능검사": [
        "2.1 검사절차 및 확인사항",
        "2.2 검사방법",
        "2.3 참고사항"
    ],
    "3. 정기검사": [
        "3.1 검사절차 및 확인사항",
        "3.2 검사방법",
        "3.3 참고사항"
    ],
    "4. 부록": [
        "4.1 소방청 질의회신 및 협의사항",
        "4.2 검사관련 규격 및 기술지침",
        "4.3 검사 부적합 사례 및 실무 팁"
    ]
}

if "page" not in st.session_state:
    st.session_state.page = "목차"

def go_home():
    st.session_state.page = "목차"

def go_page(p):
    st.session_state.page = p

# ---------- 목차 ---------- #
if st.session_state.page == "목차":
    st.markdown('<div class="big-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    st.markdown("아래에서 원하는 항목을 선택해 주세요.")
    for main, subs in sections.items():
        st.subheader(main)
        for sub in subs:
            if st.button(sub, use_container_width=True):
                go_page(sub)

# ---------- 본문 ---------- #
else:
    current = st.session_state.page
    st.markdown(f'<div class="big-title">{current}</div>', unsafe_allow_html=True)

    def show_image(path, caption=""):
        st.markdown('<div class="img-box">🖼️ <b>이미지 영역</b></div>', unsafe_allow_html=True)
        st.image(path, use_container_width=True, caption=caption)

    # 섹션별 내용
    if current.startswith("1.1"):
        show_image("images/distance.png", "안전거리 및 보유공지")
        st.write("- 위험물탱크의 안전거리와 보유공지 기준을 설명합니다.")
        st.markdown("""
        **안전거리·보유공지 기준표**

        | 구분         | 기준    | 비고                       |
        |--------------|--------|-----------------------------|
        | 위험물 제1류 | 5m 이상 | 종류별 차등 적용            |
        | 위험물 제2류 | 3m 이상 | 인화점·저장량 따라 조정 가능 |
        | 위험물 제4류 | 6m 이상 | 옥외탱크저장소 특례 참고    |
        """)
    elif current.startswith("1.2"):
        show_image("images/sign.png", "표지 및 게시판")
        st.write("- 표지 및 게시판 설치 기준을 설명합니다.")
    elif current.startswith("1.3"):
        show_image("images/structure.png", "외부구조 및 설비")
        st.write("- 외부구조 및 설비를 설명합니다.")
    elif current.startswith("1.4"):
        show_image("images/dyke.png", "방유제")
        st.write("- 방유제 설계 및 설치 기준입니다.")
    elif current.startswith("1.5"):
        show_image("images/special.png", "옥외탱크저장소의 특례")
        st.write("- 옥외탱크저장소 특례사항입니다.")
    elif current.startswith("1.6"):
        show_image("images/fire.png", "소화설비")
        st.write("- 소화설비 기준을 설명합니다.")

    elif current.startswith("2.1"):
        show_image("images/procedure.png", "검사절차 및 확인사항")
        st.write("- 안전성능검사 절차 및 확인사항입니다.")
    elif current.startswith("2.2"):
        show_image("images/method.png", "검사방법")
        st.write("- 안전성능검사 방법을 설명합니다.")
    elif current.startswith("2.3"):
        show_image("images/reference.png", "참고사항")
        st.write("- 안전성능검사 참고사항입니다.")

    elif current.startswith("3.1"):
        show_image("images/reg_procedure.png", "정기검사 절차")
        st.write("- 정기검사 절차 및 확인사항입니다.")
    elif current.startswith("3.2"):
        show_image("images/reg_method.png", "정기검사 방법")
        st.write("- 정기검사 방법을 설명합니다.")
    elif current.startswith("3.3"):
        show_image("images/reg_reference.png", "정기검사 참고사항")
        st.write("- 정기검사 참고사항입니다.")

    elif current.startswith("4.1"):
        show_image("images/query.png", "소방청 질의회신 및 협의사항")
        st.write("- 소방청 질의회신 및 협의사항을 정리합니다.")
    elif current.startswith("4.2"):
        show_image("images/standard.png", "검사관련 규격 및 기술지침")
        st.write("- 검사관련 규격 및 기술지침을 소개합니다.")
    elif current.startswith("4.3"):
        show_image("images/case.png", "검사 부적합 사례 및 실무 팁")
        st.write("- 검사 부적합 사례와 실무 팁을 정리합니다.")
    else:
        show_image("images/location.png", "샘플 이미지")
        st.write("이 섹션의 상세 내용을 여기에 추가하세요.")

    # 목차로 돌아가기
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("🏠 목차로 돌아가기", use_container_width=True):
        go_home()
