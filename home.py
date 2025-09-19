import streamlit as st
import os, glob

st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="wide")

# ---------- 스타일 ---------- #
st.markdown("""
<style>
.title {text-align:center; font-size:2.2rem; font-weight:800; color:#003366; margin-bottom:1.2em;}
.sub-title {text-align:center; font-size:1.1rem; color:#444; margin-bottom:1.5em;}
.section-title {color:#003366; font-weight:700; margin-top:1.2em; font-size:1.1rem;}
.stButton button {width:100%; border-radius:8px; background-color:#005bac; color:white;
    border:none; padding:0.7em; font-size:1rem; font-weight:600; margin-bottom:0.4em;}
.stButton button:hover {background-color:#0072e0;}
.img-box {background-color:#ffffff; border:1.5px solid #d0d7e2; border-radius:10px;
    padding:1em; margin:1.2em 0; box-shadow:0 2px 6px rgba(0,0,0,0.08);}
table {width:100%; border-collapse:collapse; margin-top:0.5em;}
table th, table td {border:1px solid #d0d7e2; padding:8px; text-align:center;}
table th {background-color:#005bac; color:white;}
table tr:nth-child(even){background-color:#f0f4f8;}
.back-btn button {background-color:#005bac; color:white; border-radius:6px;
    padding:0.6em 1em; border:none; font-weight:600;}
.back-btn button:hover {background-color:#0072e0;}
</style>
""", unsafe_allow_html=True)

# ---------- 데이터 ---------- #
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

if "page" not in st.session_state:
    st.session_state.page = "목차"

def go_home():
    st.session_state.page = "목차"

def go_page(name):
    st.session_state.page = name

# ---------- 이미지 탐색 ---------- #
def find_image(name):
    exts = ['jpg','jpeg','png']
    for e in exts:
        p = f"images/{name}.{e}"
        if os.path.exists(p):
            return p
    for e in exts:
        g = glob.glob(f"images/{name}*.{e}")
        if g:
            return g[0]
    return None

# ---------- 메인 타이틀 ---------- #
st.markdown('<div class="title">📘 클릭하며 배우는 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">아래 목차를 클릭하면 해당 내용이 바로 나타납니다.</div>',
            unsafe_allow_html=True)

# ---------- 목차 (전체 노출) ---------- #
if st.session_state.page == "목차":
    for main, subs in sections.items():
        st.subheader(main)
        for sub in subs:
            st.button(sub, use_container_width=True,
                      key=f"menu-{sub}", on_click=go_page, args=(sub,))

# ---------- 본문 ---------- #
else:
    current = st.session_state.page
    st.markdown(f"### {current}")

    def show_image(name, caption=""):
        img_path = find_image(name)
        if img_path:
            st.image(img_path, use_container_width=True, caption=caption)

    # 섹션별 예시
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
        if st.button("➡️ 방화상 유효한 담 (부록 4.1)",
                     use_container_width=True, key="b-4.1"):
            go_page("4.1 소방청 질의회신 및 협의사항")

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
        if st.button("➡️ 검사관련 규격 참고 (부록 4.2)",
                     use_container_width=True, key="b-4.2"):
            go_page("4.2 검사관련 규격 및 기술지침")

    elif current.startswith("4.1"):
        show_image("소방청 질의회신 및 협의사항","부록 4.1")
        st.write("소방청 질의회신 및 협의사항을 정리합니다.")

    # ...다른 섹션도 위와 같은 패턴으로 추가...

    # ---- 돌아가기 ----
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기",
              use_container_width=True,
              key="back-home",
              on_click=go_home)
