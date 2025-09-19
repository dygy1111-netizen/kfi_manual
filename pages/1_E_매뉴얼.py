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

    # Streamlit 컨테이너에 적용할 공통 CSS
    st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div.card-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
    }
    .chapter-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #333333;
        margin-bottom: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

    for main, subs in sections.items():
        # 컨테이너 자체를 카드처럼 꾸미기 위해 key 부여
        with st.container():
            # div.card-box를 강제로 생성하기 위해 빈 마크다운
            st.markdown('<div class="card-box">', unsafe_allow_html=True)

            # 대분류 제목
            st.markdown(f"<div class='chapter-title'>📂 {main}</div>", unsafe_allow_html=True)

            # 소분류 버튼 (같은 컨테이너 안에 렌더링)
            for sub in subs:
                st.button(sub, key=f"menu-{sub}", use_container_width=True,
                          on_click=go_page, args=(sub,))

            # 박스 닫기
            st.markdown("</div>", unsafe_allow_html=True)







# ---------- 본문 ---------- #
else:
    current = st.session_state.page
    st.markdown(f'<div class="main-title">{current}</div>', unsafe_allow_html=True)

    # ✅ 이미지 자동 출력 함수
    def show_image_auto(key):
        # 세부 목차 이름을 안전한 파일명으로 변환
        safe_name = key.replace(" ", "_").replace("/", "_")
        img_path = find_image(safe_name)
        if img_path:
            # 이미지가 있으면 자동 출력
            st.image(img_path, use_container_width=True, caption=key)

    # 🔹항상 이미지 시도 (파일이 없으면 그냥 넘어감)
    show_image_auto(current)

    # ✅ 외부 콘텐츠 로딩 함수
    def load_content(key):
        safe_name = key.replace(" ", "_").replace("/", "_")
        path = Path(f"contents/{safe_name}.md")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    # ✅ Markdown 파일 출력
    content = load_content(current)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.warning("⚠️ 아직 준비된 내용이 없습니다.")

    # ✅ 목차로 돌아가기 버튼
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("🏠 목차로 돌아가기",
              use_container_width=True,
              key="btn-home",
              on_click=go_home)
