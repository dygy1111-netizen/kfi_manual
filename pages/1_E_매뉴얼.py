import streamlit as st
import os, glob
from pathlib import Path

# ✅ 페이지 설정
st.set_page_config(page_title="위험물탱크 E-매뉴얼", page_icon="📘", layout="wide")

# ---------- 공통 CSS ---------- #
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: #ffffff;
    line-height: 1.7;
}

/* 인트로 타이틀 */
.title-container {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
}
.main-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #222222;
    line-height: 1.4;
}
.sub-title {
    font-size: 2.0rem;
    font-weight: 800;
    color: #444444;
    line-height: 1.4;
}
.guide-text {
    text-align: center;
    font-size: 1.1rem;
    margin-top: 10px;
    line-height: 1.6;
    color: #555555;
}

/* 📘 목차 큰 박스 */
.menu-box {
    border: 2px solid #d9e6f2;
    background-color: #f8fbff;
    border-radius: 12px;
    padding: 1.2em;
    margin-top: 1.2em;
}
.menu-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #003366;
    margin-bottom: 0.8em;
    display: flex;
    align-items: center;
}
.menu-title .emoji {
    margin-right: 0.4em;
    font-size: 1.4rem;
}
.menu-btn {
    width: 100%;
    margin-bottom: 0.4em;
}

/* 📘 파란색 버튼 */
.stButton button {
    width: 100%;
    border-radius: 8px;
    background-color: #005bac;
    color: white;
    border: none;
    padding: 0.7em;
    font-size: 1rem;
    font-weight: 600;
}
.stButton button:hover { background-color: #0072e0; }

/* 본문 파란색 스타일 유지 */
.section-title {
    color:#003366;
    font-weight:700;
    margin-top:1.2em;
    font-size:1.1rem;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5em;
}
table th, table td {
    border: 1px solid #d0d7e2;
    padding: 8px;
    text-align: center;
}
table th {
    background-color: #005bac;
    color: white;
}
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

# ---------- 이미지 탐색 함수 ---------- #
def find_image(name):
    exts = ['jpg','jpeg','png']
    for e in exts:
        path = f"images/{name}.{e}"
        if os.path.exists(path):
            return path
    for e in exts:
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

# ---------- 세션 상태 ---------- #
if "page" not in st.session_state:
    st.session_state.page = "목차"

def go_home():
    st.session_state.page = "목차"
def go_page(p):
    st.session_state.page = p

# ---------- 사이드바 ---------- #
st.sidebar.title("메뉴")
if st.sidebar.button("🏠 인트로로 이동"):
    st.session_state.page = "인트로"
if st.sidebar.button("📘 매뉴얼로 이동"):
    st.session_state.page = "목차"

# ---------- 인트로 페이지 ---------- #
if st.session_state.page == "인트로":
    st.markdown("""
    <div class="title-container">
        <div class="main-title">클릭하며 배우는</div>
        <div class="sub-title">위험물탱크 E-매뉴얼</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="guide-text">
    ☰ <b>왼쪽 상단 메뉴</b>를 클릭해 📘 <b>E-매뉴얼</b><br>
    또는 💡 <b>자주하는 질문(FAQ)</b> 페이지로 이동하세요.
    </div>
    """, unsafe_allow_html=True)

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
        st.info("💡 images 폴더에 cover.jpg/png/jpeg 파일을 넣으면 표지가 표시됩니다.")
    if st.button("📘 매뉴얼 바로가기", use_container_width=True):
        go_home()

# ---------- 목차 페이지 ---------- #
elif st.session_state.page == "목차":
    st.markdown('<div class="main-title">📘 위험물탱크 E-매뉴얼</div>', unsafe_allow_html=True)
    st.markdown("아래에서 원하는 항목을 선택해 주세요.")
    for main, subs in sections.items():
        # ✅ 큰 박스 + 📘 아이콘
        st.markdown(
            f'<div class="menu-box"><div class="menu-title"><span class="emoji">📘</span>{main}</div>',
            unsafe_allow_html=True
        )
        for sub in subs:
            st.button(sub, key=f"menu-{sub}", on_click=go_page, args=(sub,))
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- 본문 ---------- #
else:
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)

    def show_image(name, caption=""):
        img_path = find_image(name)
        if img_path:
            st.image(img_path, use_container_width=True, caption=caption)
        else:
            st.warning(f"이미지를 찾을 수 없습니다: {name}")

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

    # ✅ 목차로 돌아가기
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기",
              use_container_width=True,
              key="btn-home",
              on_click=go_home)
