import streamlit as st
import os, glob

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
.section-title { color:#003366; font-weight:700; margin-top:1.2em; font-size:1.1rem; }
table { width: 100%; border-collapse: collapse; margin-top: 0.5em; }
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

# ---------- 이미지 탐색 함수 (jpg/png/jpeg 모두 허용) ---------- #
def find_image(name):
    exts = ['jpg','jpeg','png']
    for e in exts:
        path = f"images/{name}.{e}"
        if os.path.exists(path):
            return path
    for e in exts:  # 대소문자 혼합 대비
        g = glob.glob(f"images/{name}*.{e}")
        if g:
            return g[0]
    return None

# ---------- 목차 데이터 ---------- #
sections = {
    "1. 위험물탱크 위치, 구조 및 설비의 기준": [
        "1.1 안전거리",
        "1.2 보유공지",
        "1.3 표지 및 게시판",
        "1.4 외부구조 및 설비",
        "1.5 방유제",
        "1.6 옥외탱크저장소의 특례",
        "1.7 소화설비"
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

# 세션 상태
if "page" not in st.session_state:
    st.session_state.page = "목차"

def go_home():
    st.session_state.page = "목차"

def go_page(p):
    st.session_state.page = p   # on_click으로 호출 시 바로 rerun되어 즉시 반영

# ---------- 목차 ---------- #
if st.session_state.page == "목차":
    st.markdown('<div class="big-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    st.markdown("아래에서 원하는 항목을 선택해 주세요.")
    for main, subs in sections.items():
        st.subheader(main)
        for sub in subs:
            # ✅ on_click 방식 + 고유 key
            st.button(sub, use_container_width=True,
                      key=f"menu-{sub}",
                      on_click=go_page, args=(sub,))

# ---------- 본문 ---------- #
else:
    current = st.session_state.page
    st.markdown(f'<div class="big-title">{current}</div>', unsafe_allow_html=True)

    def show_image(name, caption=""):
        img_path = find_image(name)
        if img_path:
            st.image(img_path, use_container_width=True, caption=caption)
        else:
            st.warning(f"이미지를 찾을 수 없습니다: {name}")

    # ✅ 섹션별 내용 샘플 (목적·기준·부록)
    if current.startswith("1.1"):
        show_image("안전거리","안전거리")
        st.markdown('<div class="section-title">목적</div>', unsafe_allow_html=True)
        st.write("위험물탱크 간 안전거리를 확보하여 화재 확산을 방지합니다.")
        st.markdown('<div class="section-title">기준</div>', unsafe_allow_html=True)
        st.markdown("""
        | 구분 | 기준 |
        |------|------|
        | 위험물 제1류 | 5m 이상 |
        | 위험물 제2류 | 3m 이상 |
        | 위험물 제4류 | 6m 이상 |
        """)
        st.markdown('<div class="section-title">부록</div>', unsafe_allow_html=True)
        st.button("➡️ 방화상 유효한 담 (부록 4.1)",
                  use_container_width=True,
                  key="btn-4.1",
                  on_click=go_page, args=("4.1 소방청 질의회신 및 협의사항",))

    elif current.startswith("1.2"):
        show_image("보유공지","보유공지")
        st.markdown('<div class="section-title">목적</div>', unsafe_allow_html=True)
        st.write("위험물 저장량에 따라 필요 공지를 설치해 안전을 확보합니다.")
        st.markdown('<div class="section-title">기준</div>', unsafe_allow_html=True)
        st.markdown("""
        | 저장량 | 공지 너비 |
        |--------|----------|
        | 500리터 미만 | 1m |
        | 500~1000리터 | 2m |
        """)
        st.markdown('<div class="section-title">부록</div>', unsafe_allow_html=True)
        st.button("➡️ 검사관련 규격 참고 (부록 4.2)",
                  use_container_width=True,
                  key="btn-4.2",
                  on_click=go_page, args=("4.2 검사관련 규격 및 기술지침",))

    elif current.startswith("4.1"):
        show_image("소방청 질의회신 및 협의사항","부록 4.1")
        st.write("소방청 질의회신 및 협의사항을 정리합니다.")

    # (다른 항목도 동일하게 show_image('한글파일명') + st.button(on_click=...) 사용)

    # ✅ 목차로 돌아가기 버튼
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기",
              use_container_width=True,
              key="btn-home",
              on_click=go_home)
