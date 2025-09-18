import streamlit as st

# ---------------------- 페이지 기본 설정 ---------------------- #
st.set_page_config(
    page_title="클릭하며 배우는 위험물탱크 E-매뉴얼",
    page_icon="🛢️",
    layout="wide"
)

# ---------------------- 폰트 & 스타일 ---------------------- #
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Noto Sans KR', sans-serif;
            line-height: 1.6;
        }
        .big-title {
            font-size: 2rem !important;
            font-weight: 700;
            text-align: center;
            padding: 0.5em 0;
        }
        .back-btn {
            text-align: right;
            margin-top: 1.5em;
        }
        /* 🎨 이미지 박스 강조 */
        .img-box {
            background-color: #ffeeba; /* 연한 노랑 */
            border: 3px dashed #ff6b6b; /* 빨강 점선 테두리 */
            padding: 1em;
            margin: 1em 0;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 목차 데이터 ---------------------- #
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

# ---------------------- 세션 상태 ---------------------- #
if "page" not in st.session_state:
    st.session_state.page = "목차"

def go_home():
    st.session_state.page = "목차"

def go_page(p):
    st.session_state.page = p

# ---------------------- 목차 화면 ---------------------- #
if st.session_state.page == "목차":
    st.markdown('<div class="big-title">🛢️ 클릭하며 배우는 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    st.markdown("아래에서 원하는 항목을 클릭하세요.")
    for main, subs in sections.items():
        st.subheader(main)
        for sub in subs:
            if st.button(sub, use_container_width=True):
                go_page(sub)

# ---------------------- 각 섹션 화면 ---------------------- #
else:
    current = st.session_state.page
    st.markdown(f'<div class="big-title">{current}</div>', unsafe_allow_html=True)

    # ✅ 이미지 박스 강조 + 아이콘
    def show_image(path, caption=""):
        st.markdown('<div class="img-box">🖼️ <b>이미지 영역</b></div>', unsafe_allow_html=True)
        st.image(path, use_container_width=True, caption=caption)

    # ✅ 섹션별 내용 (PNG 이미지 + Markdown 표 추가)
    if current.startswith("1.1"):
        show_image("images/distance.png", "안전거리 및 보유공지")
        st.write("- 안전거리 및 보유공지 기준을 설명합니다.")

        # 📊 Markdown 표 추가
        st.markdown("""
        **안전거리·보유공지 기준표**

        | 구분           | 기준           | 비고                        |
        |----------------|----------------|------------------------------|
        | 위험물 제1류   | 5m 이상        | 종류별 차등 적용             |
        | 위험물 제2류   | 3m 이상        | 인화점·저장량에 따라 조정 가능 |
        | 위험물 제4류   | 6m 이상        | 옥외탱크저장소 특례 참고     |
        """)
        st.info("💡 Markdown 표는 모바일에서도 자동으로 폭을 맞춰 깔끔하게 표시됩니다.")

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

    # 목차로 돌아가기 버튼
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("🏠 목차로 돌아가기", use_container_width=True):
        go_home()
    st.markdown('</div>', unsafe_allow_html=True)
